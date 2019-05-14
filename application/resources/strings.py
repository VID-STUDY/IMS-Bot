import os
import json
from application.core.models import Rating, FAQ, Call, AdCampaign
from application.core.advertservice import get_coverages_by_budget
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
    if language == 'uz':
        text = rating.text_uz
    else:
        text = rating.text_ru
    return text


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


def from_notify_order(order: AdCampaign):
    template = "*Новый заказ на рекламную компанию!*\n\n"\
               "*Имя заказчика:* {name}\n"\
               "*Номер телефона:* {phone_number}\n"\
               "*Компания заказчика:* {company}\n"\
               "*Товар/услуга:* {product}\n"\
               "*Целевая аудитория:* {audience}\n"\
               "*Возраст аудитории:* {age}\n"\
               "*Бюджет:* {budget}"
    return template.format(name=order.user.name,
                           phone_number=order.user.phone_number,
                           company=order.user.company_name,
                           product=order.product_name,
                           audience=from_target_audience_enum_to_text(order.target_audience, 'ru'),
                           age=format_ages(order.age_of_audience, 'ru'),
                           budget=budget_enum_to_text(order.budget, 'ru'))


def to_target_audience_enum(text: str, language: str) -> Optional[AnyStr]:
    if get_string('campaign.male', language) == text:
        return AdCampaign.TargetAudiences.MALE
    elif get_string('campaign.female', language) == text:
        return AdCampaign.TargetAudiences.FEMALE
    elif get_string('campaign.male_and_female', language) == text:
        return AdCampaign.TargetAudiences.MALE_AND_FEMALE
    else:
        return None


def from_target_audience_enum_to_text(value: str, language: str):
    return get_string('campaign.' + value, language)


def from_ages_enum_value(value: str, language) -> str:
    return get_string('ages.' + value, language)


def to_ages_enum(text: str, language) -> Optional[AnyStr]:
    if get_string('ages.6-10', language) in text:
        return AdCampaign.AudienceAges.AGES[0]
    elif get_string('ages.11-17', language) in text:
        return AdCampaign.AudienceAges.AGES[1]
    elif get_string('ages.18-24', language) in text:
        return AdCampaign.AudienceAges.AGES[2]
    elif get_string('ages.25-34', language) in text:
        return AdCampaign.AudienceAges.AGES[3]
    elif get_string('ages.35-44', language) in text:
        return AdCampaign.AudienceAges.AGES[4]
    elif get_string('ages.45-54', language) in text:
        return AdCampaign.AudienceAges.AGES[5]
    elif get_string('ages.55_and_older', language) in text:
        return AdCampaign.AudienceAges.AGES[6]
    elif get_string('ages.all', language) in text:
        return AdCampaign.AudienceAges.ALL
    else:
        return None


def format_ages(ages_string: str, language: str) -> str:
    ages = [age.strip() for age in ages_string.split(',')]
    ages = [age for age in ages if age != '']
    text_ages = [from_ages_enum_value(age, language) for age in ages]
    text_ages_result = []
    for age in text_ages:
        if age != text_ages[-1]:
            age += ', '
        text_ages_result.append(age)
    formatted_string = ''.join(text_ages_result)
    return formatted_string


def budget_enum_to_text(value: str, language: str) -> str:
    return get_string('budget.' + value, language)


def text_to_budget_enum(text: str, language: str) -> Optional[AnyStr]:
    if get_string('budget.small', language) in text:
        return AdCampaign.BudgetOptions.SMALL
    elif get_string('budget.medium', language) in text:
        return AdCampaign.BudgetOptions.MEDIUM
    elif get_string('budget.large', language) in text:
        return AdCampaign.BudgetOptions.LARGE
    elif get_string('budget.very_large', language) in text:
        return AdCampaign.BudgetOptions.VERY_LARGE
    else:
        return None


def from_coverage_to_text(coverage: tuple, language: str) -> str:
    template = get_string('campaign.coverage', language)
    return template.format(from_value=coverage[0],
                           to_value=coverage[1])


def total_ad_order(ad_order: AdCampaign, language: str):
    template = get_string('campaign.confirmation_template', language)
    return template.format(product_name=ad_order.product_name,
                           audience=from_target_audience_enum_to_text(ad_order.target_audience, language),
                           age=format_ages(ad_order.age_of_audience, language),
                           coverage=from_coverage_to_text(get_coverages_by_budget(ad_order.budget), language),
                           budget=budget_enum_to_text(ad_order.budget, language))
