from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)

    mobile = db.Column(db.String(15))

    password = db.Column(db.String(200))

    language = db.Column(db.String(50), default="English")

    otp = db.Column(db.String(10))