from flask import Blueprint, render_template
from flask_login import login_required
from werkzeug.exceptions import NotFound

user = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@user.route('/')
@login_required
def user_list():
    from blog.models import User
    users = User.query.all()
    return render_template(
        'users/user_list.html',
        users=users,
    )


@user.route('/<int:pk>')
@user.route('/<int:pk>/')
@login_required
def user_get(pk: int):
    from blog.models import User
    user = User.query.filter_by(id=pk).one_or_none()
    if user is None:
        raise NotFound(f"User id:{pk}, not found")
    return render_template(
        'users/user_detail.html',
        user=user,
    )


# def get_user_name(pk: int):
#     if pk in USERS:
#         user_name = USERS[pk]["name"]
#     else:
#         raise NotFound("User id:{}, not found".format(pk))
#     return user_name