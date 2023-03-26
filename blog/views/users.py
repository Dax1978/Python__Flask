from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.exceptions import NotFound
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from blog import db
from blog.models import User
from blog.views.articles import articles_app


users_app = Blueprint("users_app", __name__)


@users_app.route('/register/', endpoint="register", methods=['POST', 'GET'])
def register_route():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    is_staff = True if request.form.get('is_staff') else False

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Пожалуйста заполните все поля')
        elif password != password2:
            flash('Указанные пароли не совпадают')
        else:
            hash_password = generate_password_hash(password)
            new_user = User(login=login, password=hash_password, is_staff=is_staff)
            try:
                db.session.add(new_user)
                db.session.commit()
                # return redirect('/users/login/')
                return redirect(url_for('users_app.login'))
            except:
                return "При добавлении нового пользователя произошла ошибка"

    return render_template('users/register.html')


# Если только авторизованный пользователь то декоратор
# @login_required


@users_app.route('/login/', endpoint="login", methods=['POST', 'GET'])
def login_route():
    if current_user.is_authenticated:
        return redirect(url_for('articles_app.list'))

    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')
            return redirect(next_page or url_for('articles_app.list'))
        else:
            flash('Ошибка авторизации. Укажите корректный логин и пароль')
    else:
        flash('Ошибка авторизации. Укажите логин и пароль')
    return render_template('users/login.html')

@users_app.route('/logout/', endpoint="logout", methods=['POST', 'GET'])
@login_required
def logout_route():
    logout_user()
    return redirect(url_for('index'))


# @users_app.after_request
# def redirect_to_signin(response):
#     if response.status_code == 401:
#         return redirect(url_for('login_route') + '?next=' + request.url)
#
#     return response


# USERS = {
#     1: "James",
#     2: "Brian",
#     3: "Peter",
# }
#
#
# @users_app.route("/", endpoint="list")
# def users_list():
#     return render_template("users/list.html", users=USERS)
#
#
# @users_app.route("/<int:user_id>/", endpoint="details")
# def user_details(user_id: int):
#     try:
#         user_name = USERS[user_id]
#     except KeyError:
#         raise NotFound(f"User #{user_id} doesn't exist!")
#     return render_template('users/details.html', user_id=user_id, user_name=user_name)