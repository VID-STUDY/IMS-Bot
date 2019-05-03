from application import telegram_bot as bot
from application.resources import strings, keyboards
from application.core import userservice, channelservice
from telebot.types import Message


def check_package_offers(message: Message):
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    return strings.get_string('main_menu.package_offers', language) in message.text and message.chat.type == 'private'


def check_auth(message: Message):
    return userservice.is_user_registered(message.from_user.id)


@bot.message_handler(commands=['packages'])
@bot.message_handler(content_types=['text'], func=lambda m: check_auth(m) and check_package_offers(m))
def package_offers_handler(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    channels = channelservice.get_channels_only_with_package_offers()
    if len(channels) == 0:
        empty_msg = strings.get_string('package_offers.empty', language)
        bot.send_message(chat_id, empty_msg)
        return
    channel_message = strings.get_string('package_offers.channel', language)
    channels_keyboard = keyboards.from_channels(channels)
    bot.send_message(chat_id, channel_message, reply_markup=channels_keyboard)
    bot.register_next_step_handler_by_chat_id(chat_id, channel_processor)


def channel_processor(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        error_msg = strings.get_string('package_offers.channel', language)
        bot.send_message(chat_id, error_msg)
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
        package_offers = channelservice.get_package_offers_by_channel(message.text)
    except channelservice.ChannelNotFound:
        error()
        return
    for package_offer in package_offers:
        if package_offer.telegram_id:
            bot.send_document(chat_id, package_offer.telegram_id)
        else:
            bot.send_chat_action('upload_document')
            file = open(package_offer.file_path, 'rb')
            sent_file = bot.send_document(chat_id, file)
            tg_id = sent_file.document.file_id
            channelservice.set_telegram_id_for_price_file(package_offer.id, tg_id)
    bot.register_next_step_handler_by_chat_id(chat_id, channel_processor)
