from flask import Blueprint, render_template

report = Blueprint('report', __name__, url_prefix='/reports', static_folder='../../static')


@report.route('/')
def report_list():
    return render_template(
        'reports/report_list.html'
    )