import os
import json
from application.core.models import Rating, FAQ

_basedir = os.path.abspath(os.path.dirname(__file__))

_strings_ru = json.loads(open(os.path.join(_basedir, 'strings_ru.json'), 'r').read())
_strings_uz = json.loads(open(os.path.join(_basedir, 'strings_uz.json'), 'r').read())


def get_string(key, language='ru'):
    if language == 'ru':
        return _strings_ru.get(key, 'no_string')
    elif language == 'uz':
        return _strings_uz.get(key, 'no_string')
    else:
        raise Exception('Invalid language')


def from_rating(rating: Rating, language) -> str:
    template = "{msg} {date}\n\n{text}"
    if language == 'uz':
        text = rating.text_uz
    else:
        text = rating.text_ru
    return template.format(msg=get_string('ratings.ratings_for_date', language),
                           date=rating.date.strftime('%d:%m:%Y'),
                           text=text)


def from_faq(faq: FAQ, language: str) -> str:
    if language == 'uz':
        return faq.text_uz
    else:
        return faq.text_ru
