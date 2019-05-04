from application import db
from application.core.models import FAQ


def get_faq() -> FAQ or None:
    """
    Return faq or None if faq doesn't exist
    :return: Faq or None
    """
    try:
        faq = FAQ.query.all()[0]
    except IndexError:
        return None
    return faq


def save_faq(text_ru: str, text_uz: str):
    """
    Update or create new faq
    :param text_ru: Text in russian
    :param text_uz: Text in uzbek
    :return: void
    """
    faq = get_faq()
    if faq:
        faq.text_ru = text_ru
        faq.text_uz = text_uz
    else:
        faq = FAQ(text_ru=text_ru, text_uz=text_uz)
        db.session.add(faq)
    db.session.commit()
