from flask import Blueprint, render_template, request, redirect
from flask_login import login_required

from blog import db
from blog.models import Article

articles_app = Blueprint("articles_app", __name__)


@articles_app.route("/create/", endpoint="create", methods=['POST', 'GET'])
@login_required
def article_create():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/articles/')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template('articles/create.html')


@articles_app.route("/", endpoint="list")
@login_required
def articles_list():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("articles/list.html", articles=articles)


@articles_app.route("/<int:article_id>/", endpoint="details")
@login_required
def article_details(article_id: int):
    article = Article.query.get(article_id)
    return render_template('articles/details.html', article=article)


@articles_app.route("/<int:article_id>/delete", endpoint="delete")
@login_required
def article_delete(article_id: int):
    article = Article.query.get_or_404(article_id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/articles/')
    except:
        return "При удалении статьи произошла ошибка"


@articles_app.route("/<int:article_id>/update", endpoint="update", methods=['POST', 'GET'])
@login_required
def article_update(article_id):
    article = Article.query.get(article_id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/articles/')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template('articles/update.html', article=article)


# ARTICLES = {
#     1: "Flask",
#     2: "Django",
#     3: "JSON:API",
# }
# @articles_app.route("/", endpoint="list")
# def articles_list():
#     return render_template("articles/list.html", articles=ARTICLES)
# @articles_app.route("/<int:article_id>/", endpoint="details")
# def article_details(article_id: int):
#     try:
#         article = ARTICLES[article_id]
#     except KeyError:
#         raise NotFound(f"Post #{article_id} doesn't exist!")
#     return render_template('articles/details.html', article_id=article_id, article=article)