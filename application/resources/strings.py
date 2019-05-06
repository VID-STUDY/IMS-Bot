import os
import json
from application.core.models import Rating, FAQ, Call

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
    template = "{date}\n\n{text}"
    if language == 'uz':
        text = rating.text_uz
    else:
        text = rating.text_ru
    return template.format(date=get_string('ratings.ratings_for_date', language)
                           .format(rating.date.strftime('%d.%m.%Y')),
                           text=text)


def from_faq(faq: FAQ, language: str) -> str:
    if language == 'uz':
        return faq.text_uz
    else:
        return faq.text_ru


def from_notify_call(call: Call):
    template = '<b>Новый заказ звонка!</b>\n\n' \
               '<b>Имя заказчика:</b> {name}\n' \
               '<b>Компания заказчика:</b> {company}\n' \
               '<b>Номер телефона:</b> {phone_number}\n' \
               '<b>Время звонка:</b> {time}'
    return template.format(name=call.user.name,
                           company=call.user.company_name,
                           phone_number=call.phone_number,
                           time=call.time)
