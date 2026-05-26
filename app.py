from flask import Flask
from config import Config

from extensions import db, bcrypt, jwt, mail

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    app.secret_key = "supersecret"

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    from auth import auth_bp
    from language import language_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(language_bp)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run()