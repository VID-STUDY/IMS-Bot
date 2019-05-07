from application import telegram_bot as bot
from application.resources import strings
from telebot.types import Message
from application.core import userservice


def check_law(message: Message):
    if not message.text:
        return False
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    return strings.get_string('main_menu.law_on_ad', language) in message.text and message.chat.type == 'private'


def check_auth(message: Message):
    return userservice.is_user_registered(message.from_user.id)


@bot.message_handler(commands=['law'])
@bot.message_handler(content_types=['text'], func=lambda m: check_auth(m) and check_law(m))
def law_handler(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    language = userservice.get_user_language(user_id)

    law_url = strings.get_string('law.url', language)
    bot.send_message(chat_id, law_url)
