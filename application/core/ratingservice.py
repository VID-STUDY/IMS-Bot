from application import db
from application.core.models import Rating
from application.utils import tools
from werkzeug.utils import secure_filename
from config import Config
import os

from typing import Optional


def get_rating() -> Optional[Rating]:
    """
    Get last rating
    :return: Rating or None, if rating doesn't exist
    """
    try:
        rating = Rating.query.all()[0]
    except IndexError:
        return None
    return rating


def save_rating(image):
    """
    Update or create a new rating
    :param image: image file
    :return: void
    """
    rating = get_rating()
    file_path = os.path.join(Config.UPLOAD_DIRECTORY, secure_filename(image.filename))
    tools.save_file(image, file_path, recreate=True)
    if rating:
        rating.image_id = None
        if rating.image_path:
            tools.remove_file(rating.image_path)
        rating.image_path = file_path
    else:
        rating = Rating(image_path=file_path)
        db.session.add(rating)
    db.session.commit()


def set_rating_telegram_id(telegram_id):
    rating = get_rating()
    rating.image_id = telegram_id
    db.session.commit()
