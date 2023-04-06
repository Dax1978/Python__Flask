import os

import click
from werkzeug.security import generate_password_hash

from blog.extensions import db


@click.command('create-init-user')
def create_init_user():
    """
    Инициализация базы данных и создание пользователя
    """
    from blog.models import User
    from wsgi import app

    with app.app_context():
        password = os.environ.get("ADMIN_PASSWORD") or "root_"
        password = generate_password_hash(password)
        admin = User(email='root@example.com', first_name='John', last_name='Gorbunov', password=password, staff=True)

        db.session.add(admin)
        db.session.commit()
        print("created admin:", admin)


@click.command("create-admin")
def create_admin():
    """
    Run in your terminal:
    ➜ flask create-admin
    > created admin: <User #1 'admin'>
    """
    from blog.models import User

    admin = User(email='root@example.com', first_name='John', last_name='Gorbunov', staff=True)
    admin.password = os.environ.get("ADMIN_PASSWORD") or "root_"
    db.session.add(admin)
    db.session.commit()
    print("created admin:", admin)


# @click.command("init-db", help="create all models in db")
# def init_db():
#     """
#     Run in your terminal:
#     flask init-db
#     """
#     db.create_all()
#     print("Done!")
#
#
# @click.command('create-user', help="create new user")
# @click.argument('email')
# @click.argument('password')
# def create_user(email : str, password : str):
#     """
#     :param string email:
#     :param string password:
#     :Add new user (not admin) in database:
#     """
#     from blog.models import User
#     from wsgi import app
#     with app.app_context():
#         db.session.add(
#             User(email=email, password=generate_password_hash(password))
#         )
#         db.session.commit()
#
#
# @click.command('create-superuser', help="create new superuser")
# @click.argument('email')
# @click.argument('password')
# def create_superuser(email : str, password : str):
#     """
#     :param string email:
#     :param string password:
#     :Add new admin in database:
#     """
#     from blog.models import User
#     from wsgi import app
#     with app.app_context():
#         db.session.add(
#             User(email=email, password=generate_password_hash(password), staff=True)
#         )
#         db.session.commit()
#
#
# @click.command("create-users")
# def create_users():
#     """
#     Run in your terminal:
#     flask create-users
#     > done! created users: <User #1 'admin'> <User #2 'john'>
#     """
#     from blog.models import User
#     root = User(email='root@email.ru', password=generate_password_hash('root'), staff=True)
#     john = User(email='john@email.ru', password=generate_password_hash('john'))
#     from wsgi import app
#     with app.app_context():
#         db.session.add(root)
#         db.session.add(john)
#         db.session.commit()
#         print("done! created users:", root, john)
#
#
# @click.command('create-article', help="create new article")
# @click.argument('title')
# @click.argument('brief')
# @click.argument('text')
# @click.argument('author_id')
# def create_article(title: str, brief: str, text: str, author_id: int):
#     """
#     :param title - заголовок статьи:
#     :param brief - краткое содержание статьи:
#     :param text - полный текст статьи:
#     :param author_id - id автора статьи:
#     :Добавляет статью в базу данных:
#     """
#     from blog.models import Article
#     from wsgi import app
#     with app.app_context():
#         db.session.add(
#             Article(title=title, brief=brief, text=text, author_id=author_id)
#         )
#         db.session.commit()
#
#
# COMMANDS = [init_db, create_superuser, create_user, create_users, create_article]