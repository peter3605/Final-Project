# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_talisman import Talisman

# stdlib
from datetime import datetime
import os

# local

# CSP
csp = {
    'default-src': '*',
    'img-src': '*',
    'media-src': '*',
    'script-src': '*'
}

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = "cmsc388jmail@gmail.com"
MAIL_PASSWORD = "FlaskMail"
MAIL_DEFAULT_SENDER = 'cmsc388jmail@gmail.com'

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()

from .users.routes import users
from .texts.routes import texts


def page_not_found(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config["MONGODB_HOST"] = os.getenv("MONGODB_HOST")
    app.config.from_pyfile("config.py", silent=False)
    Talisman(app, content_security_policy=csp)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(texts)
    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    return app
