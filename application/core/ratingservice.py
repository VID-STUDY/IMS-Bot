from application import db
from application.core.models import Rating


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


def save_rating(text_ru, text_uz):
    """
    Update or create a new rating
    :param text_ru: Text on russian
    :param text_uz: Text on uzbek
    :return: void
    """
    rating = get_rating()
    if rating:
        rating.text_ru = text_ru
        rating.text_uz = text_uz
    else:
        rating = Rating(text_ru=text_ru, text_uz=text_uz)
        db.session.add(rating)
    db.session.commit()
