from flask_login import UserMixin
from .app import db


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


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    staff = db.Column(db.Boolean, default=False)
    article = db.relationship('Article', backref='user_article', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.email

class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    brief = db.Column(db.Text(), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Article %d>' % self.id