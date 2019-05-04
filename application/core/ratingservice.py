from application import db
from application.core.models import Rating
from datetime import datetime


def get_rating() -> Rating or None:
    """
    Get last rating
    :return: Rating or None, if rating doesn't exist
    """
    try:
        rating = Rating.query.all()[0]
    except IndexError:
        return None
    return rating


def save_rating(date_str, text_ru, text_uz):
    """
    Update or create a new rating
    :param date_str: Date String
    :param text_ru: Text on russian
    :param text_uz: Text on uzbek
    :return: void
    """
    date = datetime.strptime(date_str, '%d.%m.%Y')
    rating = get_rating()
    if rating:
        rating.date = date
        rating.text_ru = text_ru
        rating.text_uz = text_uz
    else:
        rating = Rating(date=date, text_ru=text_ru, text_uz=text_uz)
        db.session.add(rating)
    db.session.commit()
