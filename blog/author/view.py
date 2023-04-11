from flask import Blueprint, render_template
from flask_login import login_required

from blog.models import Author

author = Blueprint("author", __name__, url_prefix='/authors', static_folder='../static')


@author.route("/", endpoint="author_list")
@login_required
def author_list():
    authors = Author.query.all()
    return render_template("authors/list.html", authors=authors)