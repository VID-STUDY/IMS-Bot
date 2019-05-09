import os
import json
from application.core.models import Rating, FAQ, Call, AdCampaign
from typing import Optional, AnyStr

_basedir = os.path.abspath(os.path.dirname(__file__))

_strings_ru = json.loads(open(os.path.join(_basedir, 'strings_ru.json'), 'r').read())
_strings_uz = json.loads(open(os.path.join(_basedir, 'strings_uz.json'), 'r').read())


def get_string(key, language='ru') -> str:
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


def to_target_audience_enum(text: str, language: str) -> Optional[AnyStr]:
    if get_string('campaign.male', language) in text:
        return AdCampaign.TargetAudiences.MALE
    elif get_string('campaign.female', language) in text:
        return AdCampaign.TargetAudiences.FEMALE
    elif get_string('campaign.male_and_female', language) in text:
        return AdCampaign.TargetAudiences.MALE_AND_FEMALE
    else:
        return None


def from_ages_enum_value(value: str, language) -> str:
    return get_string('ages.' + value, language)


def to_ages_enum(text: str, language) -> Optional[AnyStr]:
    if get_string('ages.6-10', language) in text:
        return AdCampaign.AudienceAges.ALL[0]
    elif get_string('ages.11-17', language) in text:
        return AdCampaign.AudienceAges.ALL[1]
    elif get_string('ages.18-24', language) in text:
        return AdCampaign.AudienceAges.ALL[2]
    elif get_string('ages.25-34', language) in text:
        return AdCampaign.AudienceAges.ALL[3]
    elif get_string('ages.35-44', language) in text:
        return AdCampaign.AudienceAges.ALL[4]
    elif get_string('ages.45-54', language) in text:
        return AdCampaign.AudienceAges.ALL[5]
    elif get_string('ages.55_and_older', language) in text:
        return AdCampaign.AudienceAges.ALL[6]
    else:
        return None


def format_ages(ages_string: str, language: str) -> str:
    ages = [age.strip() for age in ages_string.split(',')]
    ages = [age for age in ages if age != '']
    text_ages = [from_ages_enum_value(age, language) for age in ages]
    text_ages = [string + ', ' for string in text_ages if text_ages[-1] != string]
    formatted_string = ''.join(text_ages)
    return formatted_string
