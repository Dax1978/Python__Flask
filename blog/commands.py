import click
from werkzeug.security import generate_password_hash

from wsgi import app


@app.cli.command("init-db", help="create all models in db")
def init_db():
    from blog.app import db
    """
    Run in your terminal:
    flask init-db
    """
    db.create_all()
    print("Done!")


@app.cli.command('create-user', help="create new user")
@click.argument('email')
@click.argument('password')
def create_user(email : str, password : str):
    from blog.app import db
    from blog.models import User
    db.session.add(
        User(email=email, password=generate_password_hash(password))
    )
    db.session.commit()


@app.cli.command('create-superuser', help="create new superuser")
@click.argument('email')
@click.argument('password')
def create_superuser(email : str, password : str):
    from blog.app import db
    from blog.models import User
    db.session.add(
        User(email=email, password=generate_password_hash(password), staff=True)
    )
    db.session.commit()


@app.cli.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """
    from blog.app import db
    from blog.models import User
    admin = User(username="admin", is_staff=True)
    james = User(username="james")
    db.session.add(admin)
    db.session.add(james)
    db.session.commit()
    print("done! created users:", admin, james)


@app.cli.command('create-article', help="create new article")
@click.argument('title')
@click.argument('brief')
@click.argument('text')
@click.argument('author_id')
def create_article(title: str, brief: str, text: str, author_id: int):
    from blog.app import db
    from blog.models import Article
    db.session.add(
        Article(title=title, brief=brief, text=text, author_id=author_id)
    )
    db.session.commit()


COMMANDS = [init_db, create_superuser, create_user, create_users, create_article]