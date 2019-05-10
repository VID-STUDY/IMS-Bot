from application import telegram_bot
from config import Config
from application.core import userservice
from application.resources import strings, keyboards
from flask import Blueprint, request, abort
import telebot
import os

bp = Blueprint('bot', __name__)

from application.bot import registration, settings, calls, faq, packageoffers, prices, rating, notify, law, adcampaign

if 'PRODUCTION' in os.environ:
    @bp.route(Config.WEBHOOK_URL_PATH, methods=['POST'])
    def receive_message():
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            telegram_bot.process_new_updates([update])
            return ''
        else:
            abort(400)

    telegram_bot.remove_webhook()
    telegram_bot.set_webhook(Config.WEBHOOK_URL_BASE + Config.WEBHOOK_URL_PATH)


@telegram_bot.message_handler(content_types=['text'], func=lambda m: True)
def empty_message(message: telebot.types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    main_menu_message = strings.get_string('main_menu.choose_option', language)
    main_menu_keyboard = keyboards.get_keyboard('main_menu', language)
    telegram_bot.send_message(chat_id, main_menu_message, reply_markup=main_menu_keyboard)
    return
