from application import telegram_bot
from application.core import userservice
from application.resources import strings, keyboards
import re


def process_company_name(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        error_msg = strings.get_string('welcome.company_name', language)
        telegram_bot.send_message(chat_id, error_msg)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_company_name)

    if not message.text:
        error()
        return
    if message.text.startswith('/'):
        error()
        return
    userservice.set_user_company(user_id, message.text)
    success_message = strings.get_string('welcome.registration_successfully', language)
    main_menu_keyboard = keyboards.get_keyboard('main_menu', language)
    telegram_bot.send_message(chat_id, success_message, reply_markup=main_menu_keyboard)


def process_phone_number(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        error_msg = strings.get_string('welcome.phone_number', language)
        telegram_bot.send_message(chat_id, error_msg, parse_mode='HTML')
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_phone_number)

    if message.contact is not None:
        userservice.set_user_phone_number(user_id, message.contact.phone_number)
    else:
        if message.text is None:
            error()
            return
        else:
            match = re.match(r'\+*998\s*\d{2}\s*\d{3}\s*\d{2}\s*\d{2}', message.text)
            if match is None:
                error()
                return
            phone_number = match.group()
            userservice.set_user_phone_number(user_id, phone_number)
    next_message = strings.get_string('welcome.company_name', language)
    keyboard = keyboards.get_keyboard('remove')
    telegram_bot.send_message(chat_id, next_message, reply_markup=keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_company_name)


def process_user_name(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        error_msg = strings.get_string('welcome.user_name', language)
        telegram_bot.send_message(chat_id, error_msg)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_user_language)

    if not message.text:
        error()
        return
    if message.text.startswith('/'):
        error()
        return
    userservice.set_user_name(user_id, message.text)
    next_message = strings.get_string('welcome.phone_number', language)
    phone_keyboard = keyboards.get_keyboard('welcome.phone_number', language)
    telegram_bot.send_message(chat_id, next_message, reply_markup=phone_keyboard, parse_mode='HTML')
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_phone_number)


def process_user_language(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    def error():
        error_msg = strings.get_string('welcome.say_me_language')
        telegram_bot.send_message(chat_id, error_msg)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_user_language)

    if not message.text:
        error()
        return
    if message.text.startswith('/'):
        error()
        return
    if strings.get_string('language.russian') in message.text:
        language = 'ru'
    elif strings.get_string('language.uzbek') in message.text:
        language = 'uz'
    else:
        error()
        return
    userservice.set_user_language(user_id, language)
    next_message = strings.get_string('welcome.user_name', language)
    remove_keyboard = keyboards.get_keyboard('remove')
    telegram_bot.send_message(chat_id, next_message, reply_markup=remove_keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_user_name)


@telegram_bot.message_handler(commands=['start'], func=lambda m: m.chat.type == 'private')
def welcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if userservice.is_user_registered(user_id):
        language = userservice.get_user_language(user_id)
        main_menu_message = strings.get_string('main_menu.choose_option', language)
        main_menu_keyboard = keyboards.get_keyboard('main_menu', language)
        telegram_bot.send_message(chat_id, main_menu_message, reply_markup=main_menu_keyboard)
        return
    userservice.register_user(user_id, message.from_user.username)
    welcome_text = strings.get_string('welcome')
    language_keyboard = keyboards.get_keyboard('welcome.language')
    msg = telegram_bot.send_message(chat_id, welcome_text, parse_mode='HTML', reply_markup=language_keyboard)
    telegram_bot.register_next_step_handler(msg, process_user_language)
