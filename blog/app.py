from flask import Flask

from blog import commands
from blog.extensions import db, login_manager, migrate, csrf, admin #, flask_bcrypt
from blog.models import User


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('blog.config')
    # app.config['SECRET_KEY'] = 'nqz%i%!w_%d*#=#&!na%%fbg_yx7_fw#+#t7j8vb(e%w8lz1bm'
    # app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app


def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)
    # flask_bcrypt.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    admin.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    from blog.article.views import article
    from blog.auth.views import auth
    from blog.index.views import index
    from blog.report.views import report
    from blog.user.views import user
    from blog.author.view import author
    from blog import admin

    app.register_blueprint(article)
    app.register_blueprint(auth)
    app.register_blueprint(index)
    app.register_blueprint(report)
    app.register_blueprint(user)
    app.register_blueprint(author)

    admin.register_views()


def register_commands(app: Flask):
    app.cli.add_command(commands.create_init_user)
    app.cli.add_command(commands.create_admin)
    app.cli.add_command(commands.create_tags)