from application.admin import bp
from application.core import userservice
from flask_login import login_required
from flask import render_template


@bp.route('/users')
@login_required
def users():
    all_users = userservice.get_all_bot_users()
    return render_template('admin/users.html', title='Пользователи Telegram-bot', users=all_users, area='users')
