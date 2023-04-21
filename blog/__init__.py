from os import path

# pip install flask
from flask import Flask
# pip install flask-sqlalchemy
# pip install markupsafe==2.0.1
# https://bobbyhadz.com/blog/python-importerror-cannot-import-name-soft-unicode-from-markupsafe
# «ImportError: невозможно импортировать имя «soft_unicode» из «markupsafe» из-за того, что этот soft_unicodeметод устарел в markupsafeверсии 2.1.0.
# Чтобы устранить ошибку, запустите pip install markupsafe==2.0.1команду для установки последней версии, markupsafeподдерживающей soft_unicode.

from combojsonapi.event import EventPlugin
from combojsonapi.permission import PermissionPlugin
from combojsonapi.spec import ApiSpecPlugin

from blog import commands
from blog.extensions import db, login_manager, migrate, csrf, admin, api
from blog.Blueprints.admin.views import CustomAdminIndexView


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('blog.config')

    register_extensions(app=app)
    register_blueprints(app=app)
    register_commands(app=app)

    from .models import User, Author, Article, Tag
    create_database(app=app)

    return app


# Функция для создания базы данных
def create_database(app: Flask):
    if not path.exists(app.config['SQLALCHEMY_DATABASE_URI'][10:]):
        with app.app_context():
            db.create_all()
        # https://stackoverflow.com/questions/73968584/flask-sqlalchemy-db-create-all-got-an-unexpected-keyword-argument-app
        # db.create_all(app=app) - вызовет ошибку!
        # Flask-SQLAlchemy 3 больше не принимает apгумент для таких методов, как create_all.
        # Вместо этого всегда требуется активный контекст приложения Flask.
        # with app.app_context():
        #   db.create_all()
        print("Create database!")

    else:
        print("База данных существует!")


def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)
    admin.init_app(app)
    api.plugins = [
        EventPlugin(),
        PermissionPlugin(),
        ApiSpecPlugin(
            app=app,
            tags={
                'Tag': 'Tag API',
                'User': 'User API',
                'Author': 'Author API',
                'Article': 'Article API',
            }
        ),
    ]
    api.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    from blog.Blueprints.index.views import index
    from blog.Blueprints.auth.views import auth
    from blog.Blueprints.user.views import user
    from blog.Blueprints.author.views import author
    from blog.Blueprints.article.views import article
    from blog.Blueprints.api.views import api_blueprint
    from blog.Blueprints.report.views import report
    from blog.Blueprints import admin

    app.register_blueprint(index)
    app.register_blueprint(user)
    app.register_blueprint(auth)
    app.register_blueprint(author)
    app.register_blueprint(article)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(report)

    admin.register_views()


def register_commands(app: Flask):
    app.cli.add_command(commands.create_init_user)
    app.cli.add_command(commands.create_init_tags)