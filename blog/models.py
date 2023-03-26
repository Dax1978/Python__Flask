from datetime import datetime

from flask_login import UserMixin

from blog import db, manager


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_staff = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<User #{self.id} {self.login!r}>"


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)