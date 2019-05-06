from application import telegram_bot as bot
from application.core import channelservice, userservice
from application.resources import strings, keyboards
from telebot.types import Message


def check_prices(message: Message):
    if not message.text:
        return False
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    return strings.get_string('main_menu.prices', language) in message.text and message.chat.type == 'private'


def check_auth(message: Message):
    return userservice.is_user_registered(message.from_user.id)


@bot.message_handler(commands=['prices'])
@bot.message_handler(content_types=['text'], func=lambda m: check_auth(m) and check_prices(m))
def prices(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    channel_message = strings.get_string('prices.channel', language)
    channels = channelservice.get_channels_only_with_price_files()
    if len(channels) == 0:
        empty_msg = strings.get_string('prices.empty', language)
        bot.send_message(chat_id, empty_msg)
        return
    channels_keyboard = keyboards.from_channels(channels, language)
    bot.send_message(chat_id, channel_message, reply_markup=channels_keyboard)
    bot.register_next_step_handler_by_chat_id(chat_id, channel_processor)


def channel_processor(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        error_message = strings.get_string('prices.channel', language)
        bot.send_message(chat_id, error_message)
        bot.register_next_step_handler_by_chat_id(chat_id, channel_processor)

    if not message.text:
        error()
        return
    if strings.get_string('go_back', language) in message.text:
        main_menu_message = strings.get_string('main_menu.choose_option', language)
        main_menu_keyboard = keyboards.get_keyboard('main_menu', language)
        bot.send_message(chat_id, main_menu_message, reply_markup=main_menu_keyboard)
        return
    try:
        price_files = channelservice.get_prices_by_channel(message.text)
    except channelservice.ChannelNotFound:
        error()
        return
    for price_file in price_files:
        if price_file.telegram_id:
            bot.send_document(chat_id, price_file.telegram_id)
        else:
            bot.send_chat_action(chat_id, 'upload_document')
            file = open(price_file.file_path, 'rb')
            sent_file = bot.send_document(chat_id, file)
            tg_id = sent_file.document.file_id
            channelservice.set_telegram_id_for_price_file(price_file.id, tg_id)
    bot.register_next_step_handler_by_chat_id(chat_id, channel_processor)
