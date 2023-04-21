from datetime import datetime

# pip install flask-login
# pip install markupsafe==2.0.1
# https://bobbyhadz.com/blog/python-importerror-cannot-import-name-soft-unicode-from-markupsafe
# «ImportError: невозможно импортировать имя «soft_unicode» из «markupsafe» из-за того, что этот soft_unicodeметод устарел в markupsafeверсии 2.1.0.
# Чтобы устранить ошибку, запустите pip install markupsafe==2.0.1команду для установки последней версии, markupsafe поддерживающей soft_unicode.
from flask_login import UserMixin
from sqlalchemy import Table

from blog import db
# from blog.extensions import flask_bcrypt


# https://flask-sqlalchemy-russian.readthedocs.io/ru/latest/models.html
# https://pythonru.com/biblioteki/shemy-v-sqlalchemy-orm
"""
ОДИН-КО-МНОГИМ
В общем, правильный вариант следующий:
Если есть связь 1:m, то в таблице где 1 мы устанавливаем:
    <название поля(любое)> = db.relationship(
        <Название таблицы m>,
        backref=<уникальное название для этой связи>
    )
    backref обязательно должен быть уникальным, иначе возникнет ошибка, что такая связь уже существует. 
    Т.е. если у вас, например, есть модель User и она связывается с таблицами Posts и Followers,
    то backref будет не user, а user_posts и user_followers к примеру.
В таблице со связью m мы задаём:
    db.Column(
        <тип поля id со связью 1>,
        db.ForeignKey('user.id')
    )
    значение foreignkey равно названию сущности:
        "название таблицы . название поля первичного ключа"
Если мы хотим задать связь 1:1, то в relationship ещё одним аргументом ставим uselist=False.
"""


article_tag = db.Table('article_tag',
    db.Column("article_id", db.Integer, db.ForeignKey("article.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True)
    )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, default="", server_default="")
    first_name = db.Column(db.String(120), unique=False, nullable=False, default="", server_default="")
    last_name = db.Column(db.String(120), unique=False, nullable=False, default="", server_default="")
    password = db.Column(db.String(255), nullable=False)
    staff = db.Column(db.Boolean, default=False)
    author = db.relationship("Author", uselist=False, backref='user')

    def __init__(self, email, first_name, last_name, password, staff = False):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.staff = staff

    def __repr__(self):
        return f'User: {self.first_name} {self.last_name}'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    brief = db.Column(db.Text(), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    dt_created = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    dt_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tags = db.relationship("Tag", secondary="article_tag", back_populates="articles")

    def __repr__(self):
        return '<Article %d>' % self.id

    def __str__(self):
        return str(self.id) + ' ' + self.title


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    article = db.relationship("Article", backref='author')

    def __repr__(self):
        return f'Author: {self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=False)

    articles = db.relationship("Article", secondary="article_tag", back_populates="tags")

    def __str__(self):
        return self.name