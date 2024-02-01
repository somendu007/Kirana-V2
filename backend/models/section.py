from extensions import db


class Section(db.Model):

    # init
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    unit = db.Column(db.String(100), nullable=False)
    products = db.relationship(
        "Product", back_populates="section")

    def toJson(self):
        return {
            'id': self.id,
            'name': self.name,
            'unit': self.unit,
            "numOfProducts": len(self.products)
        }
