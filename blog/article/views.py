from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import logout_user, login_user, login_required
from werkzeug.exceptions import NotFound

# from ..user.views import get_user_name

article = Blueprint('article', __name__, url_prefix='/articles', static_folder='../static')


@article.route('/')
@login_required
def article_list():
    from blog.models import User, Article
    users = User.query.all()
    articles = Article.query.all()
    return render_template(
        'articles/article_list.html',
        users=users,
        articles=articles,
    )


@article.route('/<int:pk>')
@article.route('/<int:pk>/')
@login_required
def article_get(pk: int):
    from blog.models import User, Article

    article = Article.query.filter_by(id=pk).one_or_none()
    author = User.query.get(article.author_id)
    if not article:
        raise NotFound(f"Article #{pk} doesn't exist!")
    return render_template(
        'articles/article_detail.html',
        author=author,
        article=article,
    )