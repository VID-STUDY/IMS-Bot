from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from application.resources.strings import get_string, from_ages_enum_value, from_target_audience_enum_to_text, \
    budget_enum_to_text
from application.core.models import AdCampaign

_keyboards_ru = {
    'remove': ReplyKeyboardRemove()
}
_keyboards_uz = {
    'remove': ReplyKeyboardRemove()
}

_default_value = ReplyKeyboardMarkup(resize_keyboard=True)
_default_value.add('no_keyboard')

# Initialization russian keyboards
_welcome_language = ReplyKeyboardMarkup(resize_keyboard=True)
_welcome_language.add(get_string('language.russian'), get_string('language.uzbek'))
_keyboards_ru['welcome.language'] = _welcome_language
_welcome_phone_number_ru = ReplyKeyboardMarkup(resize_keyboard=True)
_welcome_phone_number_ru.add(KeyboardButton(get_string('my_number'), request_contact=True))
_keyboards_ru['welcome.phone_number'] = _welcome_phone_number_ru
_main_menu_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
_main_menu_ru.add(get_string('main_menu.ad_campaign'),
                  get_string('main_menu.calls'),
                  get_string('main_menu.prices'),
                  get_string('main_menu.package_offers'),
                  get_string('main_menu.rating'),
                  get_string('main_menu.faq'),
                  get_string('main_menu.law_on_ad'),
                  get_string('main_menu.settings'))
_keyboards_ru['main_menu'] = _main_menu_ru
_settings_ru = ReplyKeyboardMarkup(resize_keyboard=True)
_settings_ru.add(get_string('settings.change_user_name'), get_string('settings.change_phone_number'))
_settings_ru.add(get_string('settings.change_company_name'), get_string('settings.change_language')),
_settings_ru.add(get_string('go_back'))
_keyboards_ru['settings'] = _settings_ru
_go_back_ru = ReplyKeyboardMarkup(resize_keyboard=True)
_go_back_ru.add(get_string('go_back'))
_keyboards_ru['go_back'] = _go_back_ru
_settings_change_phone_ru = ReplyKeyboardMarkup(resize_keyboard=True)
_settings_change_phone_ru.add(KeyboardButton(get_string('my_number'), request_contact=True))
_settings_change_phone_ru.add(get_string('go_back'))
_keyboards_ru['settings.change_phone'] = _settings_change_phone_ru
_settings_choose_language_ru = ReplyKeyboardMarkup(resize_keyboard=True)
_settings_choose_language_ru.add(get_string('language.russian'))
_settings_choose_language_ru.add(get_string('language.uzbek'))
_settings_choose_language_ru.add(get_string('go_back'))
_keyboards_ru['settings.choose_language'] = _settings_choose_language_ru
_call_number_keyboard_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
_call_number_keyboard_ru.add(KeyboardButton(get_string('my_number'), request_contact=True),
                             get_string('go_back'))
_keyboards_ru['call.number'] = _call_number_keyboard_ru
_call_time_keyboard_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
_call_time_keyboard_ru.add(get_string('call.in_5_minutes'),
                           get_string('call.in_10_minutes'),
                           get_string('go_back'))
_keyboards_ru['call.time'] = _call_time_keyboard_ru
_target_audience_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
_target_audience_ru.add(from_target_audience_enum_to_text(AdCampaign.TargetAudiences.MALE, 'ru'),
                        from_target_audience_enum_to_text(AdCampaign.TargetAudiences.FEMALE, 'ru'),
                        from_target_audience_enum_to_text(AdCampaign.TargetAudiences.MALE_AND_FEMALE, 'ru'))
_target_audience_ru.add(get_string('go_back'), get_string('main_menu'))
_keyboards_ru['campaign.target_audience'] = _target_audience_ru
_budget_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
_budget_ru.add(budget_enum_to_text(AdCampaign.BudgetOptions.SMALL, 'ru'))
_budget_ru.add(budget_enum_to_text(AdCampaign.BudgetOptions.MEDIUM, 'ru'))
_budget_ru.add(budget_enum_to_text(AdCampaign.BudgetOptions.LARGE, 'ru'))
_budget_ru.add(budget_enum_to_text(AdCampaign.BudgetOptions.VERY_LARGE, 'ru'))
_budget_ru.add(get_string('go_back'), get_string('main_menu'))
_keyboards_ru['campaign.budget'] = _budget_ru
_coverage_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
_coverage_ru.add(get_string('campaign.show'))
_coverage_ru.add(get_string('go_back'), get_string('main_menu'))
_keyboards_ru['campaign.coverage'] = _coverage_ru
_confirmation_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
_confirmation_ru.add(get_string('campaign.confirm'))
_confirmation_ru.add(get_string('go_back'), get_string('main_menu'))
_keyboards_ru['campaign.confirmation'] = _confirmation_ru
_rating_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
_rating_ru.add(get_string('rating.ratings'), get_string('rating.presentations'), get_string('main_menu'))
_keyboards_ru['rating'] = _rating_ru


# Initialization uzbek keybords
_welcome_phone_number_uz = ReplyKeyboardMarkup(resize_keyboard=True)
_welcome_phone_number_uz.add(KeyboardButton(get_string('my_number', 'uz'), request_contact=True))
_keyboards_uz['welcome.phone_number'] = _welcome_phone_number_uz
_main_menu_uz = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
_main_menu_uz.add(get_string('main_menu.ad_campaign', 'uz'),
                  get_string('main_menu.calls', 'uz'),
                  get_string('main_menu.prices', 'uz'),
                  get_string('main_menu.package_offers', 'uz'),
                  get_string('main_menu.rating', 'uz'),
                  get_string('main_menu.faq', 'uz'),
                  get_string('main_menu.law_on_ad', 'uz'),
                  get_string('main_menu.settings', 'uz'))
_keyboards_uz['main_menu'] = _main_menu_uz
_settings_uz = ReplyKeyboardMarkup(resize_keyboard=True)
_settings_uz.add(get_string('settings.change_user_name', 'uz'), get_string('settings.change_phone_number', 'uz'))
_settings_uz.add(get_string('settings.change_company_name', 'uz'), get_string('settings.change_language', 'uz')),
_settings_uz.add(get_string('go_back', 'uz'))
_keyboards_uz['settings'] = _settings_uz
_go_back_uz = ReplyKeyboardMarkup(resize_keyboard=True)
_go_back_uz.add(get_string('go_back', 'uz'))
_keyboards_uz['go_back'] = _go_back_uz
_settings_change_phone_uz = ReplyKeyboardMarkup(resize_keyboard=True)
_settings_change_phone_uz.add(KeyboardButton(get_string('my_number', 'uz'), request_contact=True))
_settings_change_phone_uz.add(get_string('go_back', 'uz'))
_keyboards_uz['settings.change_phone'] = _settings_change_phone_uz
_settings_choose_language_uz = ReplyKeyboardMarkup(resize_keyboard=True)
_settings_choose_language_uz.add(get_string('language.russian', 'uz'))
_settings_choose_language_uz.add(get_string('language.uzbek', 'uz'))
_settings_choose_language_uz.add(get_string('go_back', 'uz'))
_keyboards_uz['settings.choose_language'] = _settings_choose_language_uz
_call_number_keyboard_uz = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
_call_number_keyboard_uz.add(KeyboardButton(get_string('my_number', 'uz'), request_contact=True),
                             get_string('go_back', 'uz'))
_keyboards_uz['call.number'] = _call_number_keyboard_uz
_call_time_keyboard_uz = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
_call_time_keyboard_uz.add(get_string('call.in_5_minutes', 'uz'),
                           get_string('call.in_10_minutes', 'uz'),
                           get_string('go_back', 'uz'))
_keyboards_uz['call.time'] = _call_time_keyboard_uz


def get_keyboard(key, language='ru'):
    if language == 'ru':
        return _keyboards_ru.get(key, _default_value)
    elif language == 'uz':
        return _keyboards_uz.get(key, _default_value)
    else:
        raise Exception('Invalid language')


def from_channels(channels: list, language: str) -> ReplyKeyboardMarkup:
    channels_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    channels_keyboard.add(*[channel.name for channel in channels])
    channels_keyboard.add(get_string('go_back', language))
    return channels_keyboard


def from_ages(language:str, used_ages: str = None) -> ReplyKeyboardMarkup:
    age_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if used_ages and used_ages != '':
        if used_ages != AdCampaign.AudienceAges.ALL:
            user_ages = [age.strip() for age in used_ages.split(',')]
            current_ages = [age for age in user_ages if age != '']
            unused_ages = list(set(AdCampaign.AudienceAges.AGES) - set(current_ages))
            unused_ages.sort()
        else:
            unused_ages = []
    else:
        unused_ages = AdCampaign.AudienceAges.AGES
    age_keyboard.add(*[from_ages_enum_value(value, language) for value in unused_ages])
    if used_ages:
        age_keyboard.add(get_string('campaign.continue', language))
        age_keyboard.add(get_string('campaign.reset', language))
    else:
        age_keyboard.add(from_ages_enum_value(AdCampaign.AudienceAges.ALL, language))
    age_keyboard.add(get_string('go_back', language), get_string('main_menu', language))

    return age_keyboard
