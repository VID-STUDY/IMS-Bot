from application import telegram_bot as bot
from application.core import userservice, ratingservice, channelservice
from application.resources import strings, keyboards
from telebot.types import Message


def check_prices(message: Message):
    if not message.text:
        return False
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    return strings.get_string('main_menu.rating', language) in message.text and message.chat.type == 'private'


def check_auth(message: Message):
    return userservice.is_user_registered(message.from_user.id)


def _to_main_menu(chat_id, language):
    main_menu_message = strings.get_string('main_menu.choose_option', language)
    main_menu_keyboard = keyboards.get_keyboard('main_menu', language)
    bot.send_message(chat_id, main_menu_message, reply_markup=main_menu_keyboard)


@bot.message_handler(commands=['/rating'])
@bot.message_handler(content_types=['text'], func=lambda m: check_auth(m) and check_prices(m))
def rating_handler(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    rating_message = strings.get_string('rating.welcome', language)
    ratings_keyboard = keyboards.get_keyboard('rating', language)
    bot.send_message(chat_id, rating_message, reply_markup=ratings_keyboard)
    bot.register_next_step_handler_by_chat_id(chat_id, rating_processor)


def rating_processor(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        bot.register_next_step_handler_by_chat_id(chat_id, rating_processor)

    if not message.text:
        error()
        return
    if strings.get_string('main_menu', language) in message.text:
        _to_main_menu(chat_id, language)
    elif strings.get_string('rating.ratings', language) in message.text:
        rating = ratingservice.get_rating()
        if not rating:
            empty_message = strings.get_string('ratings.empty', language)
            bot.send_message(chat_id, empty_message)
            bot.register_next_step_handler_by_chat_id(chat_id, rating_processor)
            return
        rating_message = strings.from_rating(rating, language)
        bot.send_message(chat_id, rating_message, parse_mode='Markdown')
        bot.register_next_step_handler_by_chat_id(chat_id, rating_processor)
    elif strings.get_string('rating.presentations', language) in message.text:
        presentations = channelservice.get_channel_presentations()
        if len(presentations) == 0:
            presentations_empty_message = strings.get_string('rating.presentations_empty', language)
            bot.send_message(chat_id, presentations_empty_message)
            bot.register_next_step_handler_by_chat_id(chat_id, rating_processor)
        for file in presentations:
            if file.telegram_id:
                bot.send_document(chat_id, file.telegram_id)
            else:
                bot.send_chat_action(chat_id, 'upload_document')
                sent_file = bot.send_document(chat_id, open(file.file_path, 'rb'))
                tg_id = sent_file.document.file_id
                channelservice.set_telegram_id_for_presentation_file(file.id, tg_id)
        bot.register_next_step_handler_by_chat_id(chat_id, rating_processor)
    else:
        error()
