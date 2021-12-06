from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Barcode(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    brand = db.Column(db.String(140))
    barcode = db.Column(db.String(140))
    article = db.Column(db.Integer)
    size = db.Column(db.String(140))
    weigth = db.Column(db.String(140))