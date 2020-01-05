from application import db
from application.core.models import Rating, RatingImage
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


def save_rating(images):
    """
    Update or create a new rating
    :param image: image file
    :return: void
    """
    rating = get_rating()
    if not rating:
        rating = Rating()
        db.session.add(rating)
    else:
        for rating_image in rating.images.all():
            tools.remove_file(rating_image.image_path)
            db.session.delete(rating_image)
        db.session.commit()
    for image in images:
        file_path = os.path.join(Config.UPLOAD_DIRECTORY, secure_filename(image.filename))
        tools.save_file(image, file_path, recreate=True)
        rating_image = RatingImage(image_path=file_path)
        rating.images.append(rating_image)
        db.session.add(rating_image)
    db.session.commit()


def set_rating_telegram_id(image: RatingImage, telegram_id):
    image.image_id = telegram_id
    db.session.commit()
