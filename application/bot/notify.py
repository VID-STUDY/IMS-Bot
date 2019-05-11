from application import telegram_bot as bot
from application.core import notifyservice
from application.core.models import Call, AdCampaign
from application.resources import strings
from telebot.types import Message
from telebot.apihelper import ApiException


def check_group(message: Message):
    return message.chat.type == 'group' or message.chat.type == 'supergroup'


@bot.message_handler(commands=['notify'], func=check_group)
def notify_handler(message: Message):
    chat_id = message.chat.id
    chat_title = message.chat.title

    result = notifyservice.add_notify_chat(chat_id, chat_title)
    if result:
        success_message = strings.get_string('notify.registration_success')
        bot.send_message(chat_id, success_message)
    else:
        exists_message = strings.get_string('notify.exists')
        bot.send_message(chat_id, exists_message)


def notify_call(call: Call):
    notify_chats = notifyservice.get_all_notify_chats()
    notify_message = strings.from_notify_call(call)
    for chat in notify_chats:
        try:
            bot.send_message(chat.id, notify_message, parse_mode='HTML')
        except ApiException:
            pass


def notify_ad_campaign(ad_campaign: AdCampaign):
    notify_chats = notifyservice.get_all_notify_chats()
    notify_message = strings.from_notify_order(ad_campaign)
    for chat in notify_chats:
        try:
            bot.send_message(chat.id, notify_message, parse_mode='Markdown')
        except ApiException:
            pass
