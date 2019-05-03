from application import telegram_bot as bot
from application.core.models import Rating
from application.core import userservice
from application.resources import strings
from telebot.types import Message


def check_prices(message: Message):
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    return strings.get_string('main_menu.rating', language) in message.text and message.chat.type == 'private'


def check_auth(message: Message):
    return userservice.is_user_registered(message.from_user.id)


@bot.message_handler(commands=['/rating'])
@bot.message_handler(content_types=['text'], func=lambda m: check_auth(m) and check_prices(m))
def rating(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    try:
        rating_obj = Rating.query.all()[0]
    except IndexError:
        empty_message = strings.get_string('ratings.empty', language)
        bot.send_message(chat_id, empty_message)
    else:
        rating_message = strings.from_rating(rating_obj, language)
        bot.send_message(chat_id, rating_message, parse_mode='Markdown')
