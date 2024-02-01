import base64
from extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    img = db.Column(db.LargeBinary)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')
    lastLogin = db.Column(db.DateTime, nullable=False)
    ratings = db.relationship(
        "Rating", back_populates="user", lazy="dynamic"
    )

    def toJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "role": self.role,
            "email": self.email
        }

    def image(self):
        return {
            "img": base64.b64encode(self.img).decode('utf-8') if self.img != None else None,
        }

    def imgRenderReady(self):
        image = base64.b64encode(self.img).decode(
            'utf-8') if self.img != None else None
        return "data:image/png;base64,"+image
