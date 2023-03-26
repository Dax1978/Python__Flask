from flask import request, render_template
from werkzeug.exceptions import BadRequest
from flask_login import login_required

from blog import app
from blog.views.users import users_app
from blog.views.articles import articles_app


app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix="/articles")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/greet/<name>/")
@login_required
def greet_name(name: str):
    return f"Hello {name}!"


# http://127.0.0.1:5000/user/?name=John&surname=Gorbunov
@app.route("/user/")
@login_required
def read_user():
    name = request.args.get("name")
    surname = request.args.get("surname")
    return f"User {name or '[no name]'} {surname or '[no surname]'}"


@app.route("/status/", methods=["GET", "POST"])
@login_required
def custom_status_code():
    if request.method == "GET":
        return """\
        To get response with custom status code
        send request using POST method
        and pass `code` in JSON body / FormData
        """

    print("raw bytes data:", request.data)

    if request.form and "code" in request.form:
        return "code from form", request.form["code"]

    if request.json and "code" in request.json:
        return "code from json", request.json["code"]

    return "", 204


# http://127.0.0.1:5000/power/
# http://127.0.0.1:5000/power/?x=7&y=3
@app.route("/power/")
@login_required
def power_value():
    x = request.args.get("x") or ""
    y = request.args.get("y") or ""
    if not (x.isdigit() and y.isdigit()):
        app.logger.info("invalid values for power: x=%r and y=%r", x, y)
        raise BadRequest("please pass integers in `x` and `y` query params")

    x = int(x)
    y = int(y)
    result = x ** y
    app.logger.debug("%s ** %s = %s", x, y, result)
    return str(result)


# http://127.0.0.1:5000/divide-by-zero/
@app.route("/divide-by-zero/")
@login_required
def do_zero_division():
    return 1 / 0


@app.errorhandler(ZeroDivisionError)
def handle_zero_division_error(error):
    print(error) # prints str version of error: 'division by zero'
    app.logger.exception("Here's traceback for zero division error")
    return "Never divide by zero!", 400


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('examples/hello.html', name=name)