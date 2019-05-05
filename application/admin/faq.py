from application.admin import bp
from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from application.admin.forms import FaqForm
from application.core import faqservice


@login_required
@bp.route('/faq', methods=['GET', 'POST'])
def faq():
    form = FaqForm()
    if form.validate_on_submit():
        text_ru = form.text_ru.data
        text_uz = form.text_uz.data
        faqservice.save_faq(text_ru, text_uz)
        flash('Часто задоваемые вопросы изменены', category='success')
        return redirect(url_for('admin.faq'))
    current_faq = faqservice.get_faq()
    if current_faq:
        form.text_ru.data = current_faq.text_ru
        form.text_uz.data = current_faq.text_uz
    return render_template('admin/faq.html', form=form, title='FAQ', area='faq')
