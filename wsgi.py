import click
from werkzeug.security import generate_password_hash

from blog.app import create_app, db


app = create_app()
# app.run(debug=True)

@app.cli.command('init-db', help="create all models in db")
def init_db():
    db.create_all()


@app.cli.command('create-user', help="create new user")
@click.argument('email')
@click.argument('password')
def create_user(email : str, password : str):
    from blog.models import User
    db.session.add(
        User(email=email, password=generate_password_hash(password))
    )
    db.session.commit()


@app.cli.command('create-superuser', help="create new superuser")
@click.argument('email')
@click.argument('password')
def create_superuser(email : str, password : str):
    from blog.models import User
    db.session.add(
        User(email=email, password=generate_password_hash(password), staff=True)
    )
    db.session.commit()


@app.cli.command('create-article', help="create new article")
@click.argument('title')
@click.argument('brief')
@click.argument('text')
@click.argument('author_id')
def create_article(title: str, brief: str, text: str, author_id: int):
    from blog.models import Article
    db.session.add(
        Article(title=title, brief=brief, text=text, author_id=author_id)
    )
    db.session.commit()