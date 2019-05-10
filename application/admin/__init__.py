from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('admin', __name__)

from application.admin import users, calls, channels, faq, rating, orders


@bp.route('/', methods=['GET', 'HEAD'])
@login_required
def index():
    return render_template('admin/index.html')
