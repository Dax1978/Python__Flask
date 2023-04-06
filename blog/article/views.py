from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

# from ..user.views import get_user_name
from blog.models import db, Author, Article, User
from blog.forms.article import CreateArticleForm

article = Blueprint('article', __name__, url_prefix='/articles', static_folder='../static')


@article.route('/', endpoint="list")
@login_required
def articles_list():
    users = User.query.all()
    articles = Article.query.all()
    return render_template(
        'articles/article_list.html',
        users=users,
        articles=articles,
    )


@article.route('/<int:pk>', endpoint="details")
@article.route('/<int:pk>/', endpoint="details")
@login_required
def article_get(pk: int):
    article = Article.query.filter_by(id=pk).one_or_none()
    if not article:
        raise NotFound(f"Article #{pk} doesn't exist!")
    return render_template(
        'articles/details.html',
        article=article,
    )


@article.route("/create", methods=["GET", "POST"], endpoint="create")
@article.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        article = Article(title=form.title.data.strip(), brief=form.brief.data, text=form.text.data)
        db.session.add(article)
        if current_user.author:
            # use existing author if present
            article.author = current_user.author
        else:
            # otherwise create author record
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            article.author = current_user.author

        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")
            error = "Could not create article!"
        else:
            return redirect(url_for("article.details", pk=article.id))

    return render_template("articles/create.html", form=form, error=error)
