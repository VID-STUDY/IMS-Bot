from application.admin import bp
from application.core import advertservice
from flask_login import login_required
from flask import render_template, redirect, url_for, flash


@bp.route('/orders', methods=['GET'])
@login_required
def orders():
    confirmed_orders = advertservice.get_confirmed_orders()
    return render_template('/admin/orders.html', title="Рекламные кампании", orders=confirmed_orders, area='orders')


@bp.route('/order/<int:order_id>/delete', methods=['GET', 'HEAD'])
@login_required
def delete_order(order_id: int):
    advertservice.remove_order(order_id)
    flash('Заказ удалён', category='success')
    return redirect(url_for('admin.orders'))
