from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user, login_user
from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash

from blog.extensions import db
from blog.forms.user import UserRegisterForm
from blog.models import User

user = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@user.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.user_get', pk=current_user.id))

    form = UserRegisterForm(request.form)
    errors = []

    if request.method == 'POST' and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append('Email already exists')
            return render_template('users/user_register.html', form=form)

        _user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=generate_password_hash(form.password.data),
        )

        db.session.add(_user)
        db.session.commit()

        login_user(_user)

    return render_template(
        'users/user_register.html',
        form=form,
        errors=errors,
    )


@user.route('/')
@login_required
def user_list():
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
    selected_user = User.query.filter_by(id=pk).one_or_none()

    if selected_user is None:
        raise NotFound(f"User id:{pk}, not found")

    return render_template(
        'users/user_detail.html',
        user=selected_user,
    )


# def get_user_name(pk: int):
#     if pk in USERS:
#         user_name = USERS[pk]["name"]
#     else:
#         raise NotFound("User id:{}, not found".format(pk))
#     return user_name