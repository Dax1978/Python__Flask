from flask import Blueprint
from blog.Blueprints.api.tag import TagList
from blog.Blueprints.api.tag import TagDetail
from blog.Blueprints.api.user import UserList
from blog.Blueprints.api.user import UserDetail
from blog.Blueprints.api.author import AuthorList
from blog.Blueprints.api.author import AuthorDetail
from blog.Blueprints.api.article import ArticleList
from blog.Blueprints.api.article import ArticleDetail
from blog.extensions import api, csrf

api_blueprint = Blueprint('api', __name__)
csrf.exempt(api_blueprint)

api.route(TagList, 'tag_list', '/api/tags/', tag='Tag', blueprint=api_blueprint)
api.route(TagDetail, 'tag_detail', '/api/tags/<int:id>', tag='Tag', blueprint=api_blueprint)

api.route(UserList, 'user_list', '/api/users/', tag='User', blueprint=api_blueprint)
api.route(UserDetail, 'user_detail', '/api/users/<int:id>', tag='User', blueprint=api_blueprint)

api.route(AuthorList, 'author_list', '/api/authors/', tag='Author', blueprint=api_blueprint)
api.route(AuthorDetail, 'author_detail', '/api/authors/<int:id>', tag='Author', blueprint=api_blueprint)

api.route(ArticleList, 'article_list', '/api/articles/', tag='Article', blueprint=api_blueprint)
api.route(ArticleDetail, 'article_detail', '/api/articles/<int:id>', tag='Article', blueprint=api_blueprint)