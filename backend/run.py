from http.client import HTTPResponse
from flask import Flask, send_file
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from extensions import db
from flask_cors import CORS
import workers
from lib.jobs.coupon_update import updateCoupons
from celery.schedules import crontab
from lib.jobs.monthly_report import *
from lib.jobs.daily_remainder import sendMailtoUnvisitedUser
app, celery = None, None


def create_app():
    # initialization
    app = Flask(__name__)
    app.secret_key = "21f1000649"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///groceryStoreV2.db'
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_HOST'] = 'localhost'
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 0
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 500
    db.init_app(app=app)

    # initializing api
    api = Api(app=app)
    jwt = JWTManager(app=app)
    app.config['JWT_SECRET_KEY'] = '21f1000649'
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # celery setup
    celery = workers.celery
    # updating the config
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
    )
    celery.conf.beat_schedule = {
        "trigger-monthly-report": {
            "task": "lib.jobs.monthly_report.send_toAllUser",
            "schedule": crontab(minute="0", hour="0", day_of_month="1")
        },
        "trigger-daily-coupon-update": {
            "task": "lib.jobs.coupon_update.updateCoupons",
            "schedule": crontab(day_of_week="*", hour="0")
        },
        "trigger-daily-user-remainder": {
            "task": "lib.jobs.daily_remainder.sendMailtoUnvisitedUser",
            "schedule": crontab(hour="18")
        }
    }
    celery.Task = workers.ContextTask
    app.app_context().push()

    # boiler plate code for testing celery
    @app.route("/")
    def main():
        sendMailtoUnvisitedUser.delay()
        # send_report_asPDF.delay()
        return "Hello WOlrd", 200

    # importing all api resources
    from lib.api.user import UserAPI
    from lib.api.user import UserImageAPI
    from lib.api.user import UserPasswordUpdate
    # from lib.api.user import RefreshTokenAPI
    from lib.api.user import UserRatingAPI
    from lib.api.sections import SectionAPI, GetAllSections, SectionRequestsAPI
    from lib.api.approve_managers import ApproveManagerAPI
    from lib.api.approve_sectionRequests import ApproveSectionRequests
    from lib.api.products import ProductsAPI
    from lib.api.products import ProductImage
    from lib.api.products import RecentProduct
    from lib.api.cart import CartAPI
    from lib.api.buy import BuyAPI
    from lib.api.search_products import SearchProductsAPI
    from lib.api.favourites import FavouritesAPI
    from lib.api.rating import RatingsAPI
    from lib.api.coupons import CouponAPI, CouponsExtendedAPI
    # registering all the api resources
    api.add_resource(UserAPI, '/user')
    api.add_resource(UserImageAPI, '/user/img')
    api.add_resource(UserPasswordUpdate, '/user/password')
    # api.add_resource(RefreshTokenAPI, "/refresh")
    api.add_resource(UserRatingAPI, '/user/rating')
    api.add_resource(SectionAPI, '/section')
    api.add_resource(GetAllSections, '/sections')
    api.add_resource(ApproveManagerAPI, '/unapproved')
    api.add_resource(SectionRequestsAPI, '/section/request')
    api.add_resource(ApproveSectionRequests, '/section/approve')
    api.add_resource(ProductsAPI, '/product')
    api.add_resource(ProductImage, '/product/img')
    api.add_resource(RecentProduct, '/product/<limit>', endpoint='product')
    api.add_resource(CartAPI, '/cart')
    api.add_resource(BuyAPI, '/buy')
    api.add_resource(BuyAPI, '/buy/<coupon_id>', endpoint='buy')
    api.add_resource(SearchProductsAPI, '/product/search')
    api.add_resource(FavouritesAPI, '/product/favourite/<product_id>',
                     endpoint="favourite")
    api.add_resource(FavouritesAPI, '/product/favourite')
    api.add_resource(
        RatingsAPI, '/product/rating/<product_id>', endpoint='rating')
    api.add_resource(RatingsAPI, "/product/rating")
    api.add_resource(CouponAPI, '/coupon')
    api.add_resource(CouponAPI, '/coupon/<coupon_id>', endpoint='coupon')
    api.add_resource(CouponsExtendedAPI, '/coupons')
    api.add_resource(CouponsExtendedAPI,
                     "/coupons/<coupon_code>", endpoint="coupons")

    from lib.api.reports import report
    from lib.api.admin import admin
    app.register_blueprint(report)
    app.register_blueprint(admin)
    # api docs init code
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/docs/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Test application"
        }
    )
    return app, celery


def init_admin():
    from models.user import User
    if (User.query.filter_by(username='admin').first()):
        return 0
    admin = User(name='admin', username='admin',
                 password='admin', role='admin', email='admin@grocerystore.com')
    db.session.add(admin)
    db.session.commit()


app, celery = create_app()
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_admin()
    app.run(debug=True, threaded=True)
