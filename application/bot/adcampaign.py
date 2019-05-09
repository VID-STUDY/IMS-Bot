from application import telegram_bot as bot
from application.core import advertservice, userservice
from application.resources import strings, keyboards
from application.core.models import AdCampaign
from telebot.types import Message


def check_ad_campaign(message: Message):
    if not message.text:
        return False
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    return strings.get_string('main_menu.ad_campaign', language) in message.text and message.chat.type == 'private'


def check_auth(message: Message):
    return userservice.is_user_registered(message.from_user.id)


def _to_main_menu(chat_id, language, message_text=None):
    if message_text:
        main_menu_message = message_text
    else:
        main_menu_message = strings.get_string('main_menu.choose_option', language)
    main_menu_keyboard = keyboards.get_keyboard('main_menu', language)
    bot.send_message(chat_id, main_menu_message, reply_markup=main_menu_keyboard)


def _to_product_name(chat_id, language, include_keyboard=True):
    product_name_msg = strings.get_string('campaign.product_name', language)
    if include_keyboard:
        go_back_keyboard = keyboards.get_keyboard('go_back', language)
        bot.send_message(chat_id, product_name_msg, reply_markup=go_back_keyboard)
    else:
        bot.send_message(chat_id, product_name_msg)
    bot.register_next_step_handler_by_chat_id(chat_id, product_name_processor)


def _to_target_audience(chat_id, language, include_keyboard=True):
    target_audience_msg = strings.get_string('campaign.campaign.target_audience', language)
    if include_keyboard:
        target_audience_keyboard = keyboards.get_keyboard('campaign.campaign.target_audience', language)
        bot.send_message(chat_id, target_audience_msg, reply_markup=target_audience_keyboard)
    else:
        bot.send_message(chat_id, target_audience_msg)
    bot.register_next_step_handler_by_chat_id(chat_id, target_audience_processor)


def _to_audience_age(chat_id, language, include_keyboard=True, current_ad_order: AdCampaign = None):
    audience_age_msg = strings.get_string('campaign.audience_age', language)
    if include_keyboard:
        ad_campaign = current_ad_order or advertservice.get_current_campaign(chat_id)
        audience_age_keyboard = keyboards.from_ages(language, ad_campaign.age_of_audience)
        if ad_campaign.age_of_audience and ad_campaign.age_of_audience != '':
            selected_ages_template = strings.get_string('campaign.selected_ages', language)
            audience_age_msg = selected_ages_template.format(strings.format_ages(ad_campaign.age_of_audience, language))
        bot.send_message(chat_id, audience_age_msg, reply_markup=audience_age_keyboard)
    else:
        bot.send_message(chat_id, audience_age_msg)
    bot.register_next_step_handler_by_chat_id(chat_id, audience_age_processor)


def _to_budget(chat_id, language, include_keyboard=True):
    budget_msg = strings.get_string('campaign.budget', language)
    if include_keyboard:
        budget_keyboard = keyboards.get_keyboard('campaign.budget', language)
        bot.send_message(chat_id, budget_msg, reply_markup=budget_keyboard)
    else:
        bot.send_message(chat_id, budget_msg)
    bot.register_next_step_handler_by_chat_id(chat_id, budget_processor)


@bot.message_handler(commands=['campaign'])
@bot.message_handler(content_types=['text'], func=lambda m: check_ad_campaign(m) and check_auth(m))
def ad_campaign_handler(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    advertservice.create_campaign(user_id)
    _to_product_name(chat_id, language)


def product_name_processor(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    if not message.text:
        _to_product_name(chat_id, language, include_keyboard=False)
        return
    if strings.get_string('go_back', language) in message.text:
        _to_main_menu(chat_id, language)
        return
    advertservice.set_product_name(user_id, message.text)
    _to_target_audience(chat_id, language)


def target_audience_processor(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        _to_target_audience(chat_id, language, include_keyboard=True)

    if not message.text:
        error()
    enum_value = strings.to_target_audience_enum(message.text, language)
    if not enum_value:
        error()
        return
    current_ad_order = advertservice.set_target_audience(user_id, enum_value)
    _to_audience_age(chat_id, language, current_ad_order=current_ad_order)


def audience_age_processor(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        _to_audience_age(chat_id, language, include_keyboard=False)
    if not message.text:
        error()
        return
    if strings.get_string('go_back', language) in message.text:
        _to_target_audience(chat_id, language)
    elif strings.get_string('main_menu', language) in message.text:
        _to_main_menu(chat_id, language)
    elif strings.get_string('campaign.continue', language) in message.text:
        current_ad_order = advertservice.get_current_campaign(user_id)
        if current_ad_order.age_of_audience and current_ad_order.age_of_audience != '':
            _to_budget(chat_id, language)
        else:
            error()
    elif strings.get_string('campaign.reset', language) in message.text:
        current_ad_order = advertservice.reset_audience_ages(user_id)
        reset_message = strings.get_string('campaign.age_reset', language)
        bot.send_message(chat_id, reset_message)
        _to_audience_age(chat_id, language, current_ad_order=current_ad_order)
    else:
        age = strings.to_ages_enum(message.text, language)
        if not age:
            error()
        current_ad_order = advertservice.add_age_audience(user_id, age)
        _to_audience_age(chat_id, language, current_ad_order=current_ad_order)


def budget_processor(message: Message):
    pass


def coverage_processor(message: Message):
    pass


def confirmation_processor(message: Message):
    pass
