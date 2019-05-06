from application import telegram_bot as bot
from application.resources import strings
from application.core import userservice, faqservice
from telebot.types import Message


def check_faq(message: Message):
    if not message.text:
        return False
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    return strings.get_string('main_menu.faq', language) in message.text and message.chat.type == 'private'


def check_auth(message: Message):
    return userservice.is_user_registered(message.from_user.id)


@bot.message_handler(commands=['faq'])
@bot.message_handler(content_types=['text'], func=lambda m: check_auth(m) and check_faq(m))
def faq_handler(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    faq = faqservice.get_faq()
    if not faq:
        empty_msg = strings.get_string('faq.empty', language)
        bot.send_message(chat_id, empty_msg)
        return
    faq_message = strings.from_faq(faq, language)
    bot.send_message(chat_id, faq_message, parse_mode='Markdown')
