from time import time
import os

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


file_path = os.path.abspath(os.getcwd())+"/blog.db"

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.secret_key = 'super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# create the extension
db = SQLAlchemy(app)
manager = LoginManager(app)
manager.login_view = 'users_app.login'
manager.login_message = 'Авторизуйтесь для доступа к сайту'
manager.login_message_category = 'success'


from blog import models, routes, views


# Для создания БД
with app.app_context():
    db.create_all()


@app.before_request
def process_before_request():
    """
    Sets start_time to `g` object
    """
    g.start_time = time()


@app.after_request
def process_after_request(response):
    """
    adds process time in headers
    """
    if hasattr(g, "start_time"):
        response.headers["process-time"] = time() - g.start_time

    return response