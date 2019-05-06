from application import db
from application.core.models import NotifyChat


def add_notify_chat(chat_id: int, chat_title: str) -> bool:
    if NotifyChat.query.get(chat_id):
        return False
    notify_chat = NotifyChat(id=chat_id, chat_title=chat_title)
    db.session.add(notify_chat)
    db.session.commit()
    return True


def get_all_notify_chats():
    return NotifyChat.query.all()
