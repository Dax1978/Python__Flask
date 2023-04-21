from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from blog.models import User
from blog.forms.login import LoginForm


auth = Blueprint('auth', __name__, static_folder='../../static')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.user_get', pk=current_user.id))
    form = LoginForm(request.form)
    errors = []

    email = form.email.data
    password = form.password.data
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Check your login details')
        return render_template(
            'auth/login.html',
            form=form,
            errors=errors,
        )
    login_user(user)
    return redirect(url_for('user.user_get', pk=user.id))


# @auth.route('/login', methods=('GET',))
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('user.user_get', pk=current_user.id))
#
#     return render_template(
#         'auth/login.html',
#     )


# @auth.route('/login', methods=('POST',))
# def login_post():
#     email = request.form.get('email')
#     password = request.form.get('password')
#
#     user = User.query.filter_by(email=email).first()
#
#     if not user or not check_password_hash(user.password, password):
#         flash('Check your login details')
#         return redirect(url_for('.login'))
#
#     login_user(user)
#     return redirect(url_for('user.user_get', pk=user.id))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))