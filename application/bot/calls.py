from application import telegram_bot as bot
from application.resources import strings, keyboards
from application.core import callservice, userservice
from telebot.types import Message
import re


def check_calls(message: Message):
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    return strings.get_string('main_menu.calls', language) in message.text and message.chat.type == 'private'


def check_auth(message: Message):
    return userservice.is_user_registered(message.from_user.id)


def _to_phone_number(chat_id, language):
    calls_message = strings.get_string('calls.number', language)
    calls_keyboard = keyboards.get_keyboard('call.number', language)
    bot.send_message(chat_id, calls_message, parse_mode='HTML', reply_markup=calls_keyboard)
    bot.register_next_step_handler_by_chat_id(chat_id, phone_number_processor)


def _to_main_menu(chat_id, language, message_text=None):
    if message_text:
        main_menu_message = message_text
    else:
        main_menu_message = strings.get_string('main_menu.choose_option', language)
    main_menu_keyboard = keyboards.get_keyboard('main_menu', language)
    bot.send_message(chat_id, main_menu_message, reply_markup=main_menu_keyboard)


@bot.message_handler(commands=['call'])
@bot.message_handler(content_types=['text'], func=lambda m: check_auth(m) and check_calls(m))
def calls(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    callservice.make_call_by_user(user_id)
    _to_phone_number(chat_id, language)


def phone_number_processor(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        error_msg = strings.get_string('calls.number', language)
        bot.send_message(chat_id, error_msg, parse_mode='HTML')
        bot.register_next_step_handler_by_chat_id(chat_id, phone_number_processor)

    if message.contact:
        callservice.set_call_phone_number(user_id, message.contact.phone_number)
    else:
        if not message.text:
            error()
            return
        if strings.get_string('go_back', language) in message.text:
            _to_main_menu(chat_id, language)
            return
        match = re.match(r'\+*998\s*\d{2}\s*\d{3}\s*\d{2}\s*\d{2}', message.text)
        if not match:
            error()
            return
        phone_number = match.group()
        callservice.set_call_phone_number(user_id, phone_number)
    time_message = strings.get_string('call.time', language)
    time_keyboard = keyboards.get_keyboard('call.time', language)
    bot.send_message(chat_id, time_message, reply_markup=time_keyboard)
    bot.register_next_step_handler_by_chat_id(chat_id, call_time_processor)


def call_time_processor(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        error_msg = strings.get_string('call.time', language)
        bot.send_message(chat_id, error_msg)
        bot.register_next_step_handler_by_chat_id(chat_id, call_time_processor)

    if not message.text:
        error()
        return
    if strings.get_string('go_back', language) in message.text:
        _to_phone_number(chat_id, language)
        return
    callservice.set_call_time(user_id, message.text)
    callservice.confirm_call_order(user_id)
    success_message = strings.get_string('call.success', language)
    _to_main_menu(chat_id, language, success_message)
