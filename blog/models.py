from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Table

from .app import db
# from blog.extensions import flask_bcrypt


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


article_tag_association_table = Table(
    "article_tag_association",
    db.metadata,
    db.Column("article_id", db.Integer, db.ForeignKey("articles.id"), nullable=False),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), nullable=False),
)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, default="", server_default="")
    first_name = db.Column(db.String(120), unique=False, nullable=False, default="", server_default="")
    last_name = db.Column(db.String(120), unique=False, nullable=False, default="", server_default="")
    password = db.Column(db.String(255), nullable=False)
    staff = db.Column(db.Boolean, default=False)

    author = db.relationship("Author", uselist=False, backref='user_author')

    def __init__(self, email, first_name, last_name, password, staff = False):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.staff = staff

    # @property
    # def password(self):
    #     return self._password
    #
    # @password.setter
    # def password(self, value):
    #     self._password = flask_bcrypt.generate_password_hash(value)
    #
    # def validate_password(self, password) -> bool:
    #     return flask_bcrypt.check_password_hash(self._password, password)

    def __repr__(self):
        return f'User: {self.first_name} {self.last_name}'
        # return '<User %r>' % self.email

class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    brief = db.Column(db.Text(), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    dt_created = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    dt_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    tags = db.relationship(
        "Tag",
        secondary=article_tag_association_table,
        back_populates="articles",
    )

    author = db.relationship("Author", backref='article_author')

    def __repr__(self):
        return '<Article %d>' % self.id

    def __str__(self):
        return self.title


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", backref="author_user")
    article = db.relationship("Article", backref="author_article")

    def __repr__(self):
        return f'Author: {self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, default="", server_default="")
    articles = db.relationship(
        "Article",
        secondary=article_tag_association_table,
        back_populates="tags",
    )

    def __str__(self):
        return self.name