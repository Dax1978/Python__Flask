import os

from flask import Flask
import psycopg2

from json import load

from flask_login import LoginManager
from blog.extension import db, login_manager, migrate
from blog.article.views import article
from blog.models import User
from blog.user.views import user
from blog.index.views import index
from blog.report.views import report
from blog.auth.views import auth



# CONFIG_PATH = os.getenv("CONFIG_PATH", os.path.join("..\dev_config.json"))
file_path = os.path.abspath(os.getcwd())+"/db.sqlite"

VIEWS = [
    index,
    user,
    article,
    report,
    auth
]

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('blog.config')
    # app.config['SECRET_KEY'] = 'nqz%i%!w_%d*#=#&!na%%fbg_yx7_fw#+#t7j8vb(e%w8lz1bm'
    # app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    for view in VIEWS:
        app.register_blueprint(view)