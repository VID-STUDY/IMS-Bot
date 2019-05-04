from application.admin import bp
from application.core import callservice
from flask_login import login_required
from flask import render_template, redirect, url_for, flash


@bp.route('/calls', methods=['GET', 'HEAD'])
@login_required
def calls():
    confirmed_calls = callservice.get_all_confirmed_calls()
    return render_template('admin/calls.html', calls=confirmed_calls, title="Заказы звонков")


@bp.route('/call/<int:call_id>/delete', methods=['GET', 'HEAD'])
@login_required
def delete_call(call_id: int):
    callservice.remove_call(call_id)
    flash('Заказ на вызов удалён', category='success')
    return redirect(url_for('admin.calls'))
