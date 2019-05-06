from application.core import userservice
from application.auth import bp
from application.auth.forms import LoginEmailForm, LoginPasswordForm, CreateNewPasswordForm
from flask_login import login_required, current_user, login_user, logout_user
from flask import redirect, url_for, render_template, flash


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginEmailForm()
    if form.validate_on_submit():
        user = userservice.get_admin_user_by_email(form.email.data)
        if user.password_hash is None:
            return redirect(url_for('auth.set_password', user_id=user.id))
        else:
            return redirect(url_for('auth.password', user_id=user.id))
    return render_template('auth/login.html', title='Вход в систему', form=form)


@bp.route('/setpassword/<int:user_id>', methods=['GET', 'POST'])
def set_password(user_id: int):
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    user = userservice.get_admin_user_by_id(user_id)
    if not user:
        flash('Такого пользователя не существует', category='error')
        return redirect(url_for('auth.login'))
    form = CreateNewPasswordForm()
    if form.validate_on_submit():
        userservice.set_user_admin_password(user, form.password.data)
        flash('Пароль установлен', category='success')
        return redirect(url_for('auth.password', user_id=user_id))
    return render_template('auth/setpassword.html', title='Установка пароля', form=form, email=user.email)


@bp.route('/password/<int:user_id>', methods=['GET', 'POST'])
def password(user_id: int):
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    user = userservice.get_admin_user_by_id(user_id)
    if not user:
        flash('Такого пользователя не существует', category='error')
        return redirect(url_for('auth.login'))
    if not user.password_hash:
        flash('Сначала установите пароль для этого пользователя', category='warning')
        return redirect(url_for('auth.set_password', user_id=user_id))
    form = LoginPasswordForm()
    if form.validate_on_submit():
        if not user.check_password(form.password.data):
            flash('Указан неверный пароль', category='error')
            return redirect(url_for('auth.password', user_id=user_id))
        login_user(user)
        return redirect(url_for('admin.index'))
    return render_template('auth/password.html', title='Укажите пароль', form=form, email=user.email)
