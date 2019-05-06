from application.resources import strings, keyboards
from application.core import userservice
from application import telegram_bot
from telebot.types import Message
import re


def check_settings(message: Message):
    if not message.text:
        return False
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    return strings.get_string('main_menu.settings', language) in message.text and message.chat.type == 'private'


def check_auth(message: Message):
    return userservice.is_user_registered(message.from_user.id)


def back_to_the_settings_menu(chat_id, language, message_txt=None):
    if not message_txt:
        settings_message = strings.get_string('main_menu.settings', language)
    else:
        settings_message = message_txt
    settings_keyboard = keyboards.get_keyboard('settings', language)
    telegram_bot.send_message(chat_id, settings_message, reply_markup=settings_keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_choose_option)


def process_change_user_name(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        error_msg = strings.get_string('settings.send_name', language)
        telegram_bot.send_message(chat_id, error_msg)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_change_user_name)

    if not message.text:
        error()
        return
    if message.text.startswith('/'):
        error()
        return
    if strings.get_string('go_back', language) in message.text:
        back_to_the_settings_menu(chat_id, language)
        return
    userservice.set_user_name(user_id, message.text)
    success_message = strings.get_string('settings.success_change_name', language)
    back_to_the_settings_menu(chat_id, language, success_message)


def process_change_user_phone_number(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        error_msg = strings.get_string('settings.send_phone_number', language)
        telegram_bot.send_message(chat_id, error_msg, parse_mode='HTML')
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_change_user_phone_number)

    if message.contact:
        userservice.set_user_phone_number(user_id, message.contact.phone_number)
    else:
        if not message.text:
            error()
            return
        if strings.get_string('go_back', language) in message.text:
            back_to_the_settings_menu(chat_id, language)
            return
        match = re.match(r'\+*998\s*\d{2}\s*\d{3}\s*\d{2}\s*\d{2}', message.text)
        if not match:
            error()
            return
        phone_number = match.group()
        userservice.set_user_phone_number(user_id, phone_number)
    success_message = strings.get_string('settings.success_change_phone_number', language)
    back_to_the_settings_menu(chat_id, language, success_message)


def process_change_user_company_name(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        error_msg = strings.get_string('settings.send_company_name')
        telegram_bot.send_message(chat_id, error_msg)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_change_user_company_name)

    if not message.text:
        error()
        return
    if message.text.startswith('/'):
        error()
        return
    if strings.get_string('go_back', language) in message.text:
        back_to_the_settings_menu(chat_id, language)
        return
    userservice.set_user_company(user_id, message.text)
    success_message = strings.get_string('settings.success_change_company_name', language)
    back_to_the_settings_menu(chat_id, language, success_message)


def process_change_user_language(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        error_msg = strings.get_string('settings.choose_language')
        telegram_bot.send_message(chat_id, error_msg)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_change_user_language)

    if not message.text:
        error()
        return
    if strings.get_string('go_back', language) in message.text:
        back_to_the_settings_menu(chat_id, language)
    elif strings.get_string('language.russian') in message.text:
        new_language = 'ru'
        userservice.set_user_language(user_id, new_language)
        success_message = strings.get_string('settings.success_change_language', new_language)
        back_to_the_settings_menu(chat_id, new_language, success_message)
    elif strings.get_string('language.uzbek') in message.text:
        new_language = 'uz'
        userservice.set_user_language(user_id, new_language)
        success_message = strings.get_string('settings.success_change_language', new_language)
        back_to_the_settings_menu(chat_id, new_language, success_message)
    else:
        error()


def process_choose_option(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        error_msg = strings.get_string('main_menu.choose_option', language)
        telegram_bot.send_message(chat_id, error_msg)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_choose_option)

    if not message.text:
        error()
        return
    if strings.get_string('go_back', language) in message.text:
        main_menu_message = strings.get_string('main_menu.choose_option', language)
        main_menu_keyboard = keyboards.get_keyboard('main_menu', language)
        telegram_bot.send_message(chat_id, main_menu_message, reply_markup=main_menu_keyboard)
    elif strings.get_string('settings.change_user_name', language) in message.text:
        send_name_message = strings.get_string('settings.send_name', language)
        go_back_keyboard = keyboards.get_keyboard('go_back', language)
        telegram_bot.send_message(chat_id, send_name_message, reply_markup=go_back_keyboard)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_change_user_name)
    elif strings.get_string('settings.change_phone_number', language) in message.text:
        send_phone_message = strings.get_string('settings.send_phone_number', language)
        phone_number_keyboard = keyboards.get_keyboard('settings.change_phone', language)
        telegram_bot.send_message(chat_id, send_phone_message, reply_markup=phone_number_keyboard, parse_mode='HTML')
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_change_user_phone_number)
    elif strings.get_string('settings.change_company_name', language) in message.text:
        send_company_name_message = strings.get_string('settings.send_company_name', language)
        go_back_keyboard = keyboards.get_keyboard('go_back', language)
        telegram_bot.send_message(chat_id, send_company_name_message, reply_markup=go_back_keyboard)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_change_user_company_name)
    elif strings.get_string('settings.change_language', language) in message.text:
        choose_language_message = strings.get_string('settings.choose_language', language)
        choose_language_keyboard = keyboards.get_keyboard('settings.choose_language', language)
        telegram_bot.send_message(chat_id, choose_language_message, reply_markup=choose_language_keyboard)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_change_user_language)
    else:
        error()


@telegram_bot.message_handler(commands=['settings'], func=check_auth)
@telegram_bot.message_handler(content_types=['text'], func=lambda m: check_settings(m) and check_auth(m))
def main_menu_settings(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    settings_message = strings.get_string('main_menu.settings', language)
    settings_keyboard = keyboards.get_keyboard('settings', language)
    telegram_bot.send_message(chat_id, settings_message, reply_markup=settings_keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_choose_option)
