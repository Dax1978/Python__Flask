from typing import Dict

import requests
from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

# from ..user.views import get_user_name
from blog.extensions import db
from blog.models import Author, Article, User, Tag
from blog.forms.article import CreateArticleForm

article = Blueprint('article', __name__, url_prefix='/articles', static_folder='../../static')


@article.route('/', endpoint="list")
@login_required
def articles_list():
    users = User.query.all()
    articles = Article.query.all()
    # call RPC method
    count_articles: Dict = requests.get('http://127.0.0.1:5000/api/articles/event_get_count/').json()
    return render_template(
        'articles/article_list.html',
        users=users,
        articles=articles,
        count_articles=count_articles['count'],
    )


@article.route('/<int:pk>', endpoint="details", methods=['GET'])
@article.route('/<int:pk>/', endpoint="details", methods=['GET'])
@login_required
def article_get(pk: int):
    article = Article.query.filter_by(id=pk).options(
        joinedload(Article.tags)  # подгружаем связанные теги!
    ).one_or_none()

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
    # добавляем доступные теги в форму
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]

    if request.method == "POST" and form.validate_on_submit(): # при создании статьи
        article = Article(title=form.title.data.strip(), brief=form.brief.data, text=form.text.data)

        if current_user.author:
            # use existing author if present
            article.author = current_user.author
        else:
            # otherwise create author record
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            # article.author = current_user.author
            # выше не работает, т.к. возвращает None
            new_author = Author.query.filter_by(user_id=current_user.id).one_or_none()
            article.author = new_author

        if form.tags.data:  # если в форму были переданы теги (были выбраны)
            # print("form.tags.data:")
            # print(form.tags.data)

            selected_tags = []
            all_tags = Tag.query.all()  # get all tags
            # loop through all the tags
            for t in all_tags:
                if t.id in form.tags.data:
                    selected_tags.append(t)  # if the tag's id is in list "form.tags.data" append to list "selected_tags"

            # selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            # print("Tags selected_tags!!!")
            # print(selected_tags)
            article.tags.extend(selected_tags)
            # for tag in selected_tags:
            #     article.tags.append(tag)  # добавляем выбранные теги к статье


        db.session.add(article)

        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")
            error = "Could not create article!"
        else:
            return redirect(url_for("article.details", pk=article.id))

    return render_template("articles/create.html", form=form, error=error)
