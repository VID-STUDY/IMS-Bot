from application.admin import bp
from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from application.admin.forms import RatingForm
from application.core import ratingservice


@login_required
@bp.route('/rating', methods=['GET', 'POST'])
def ratings():
    rating_form = RatingForm()
    if rating_form.validate_on_submit():
        date = rating_form.date.data
        text_ru = rating_form.text_ru.data
        text_uz = rating_form.text_uz.data
        ratingservice.save_rating(date, text_ru, text_uz)
        flash('Рейтинг обновлён', category='success')
        return redirect(url_for('admin.ratings'))
    rating = ratingservice.get_rating()
    if rating:
        rating_form.date.data = rating.date.strftime('%d.%m.%Y')
        rating_form.text_ru.data = rating.text_ru
        rating_form.text_uz.data = rating.text_uz
    return render_template('admin/rating.html', title='Рейтинги', form=rating_form)
