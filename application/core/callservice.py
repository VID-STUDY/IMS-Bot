from application import db
from application.core.models import Call
from . import userservice
from datetime import datetime


def _get_current_user_call(user_id: int) -> Call:
    """
    Return current not confirmed user's call
    :param user_id: User's Telegram-ID
    :return: void
    """
    user = userservice.get_user_by_id(user_id)
    return user.calls.filter(Call.confirmed != True).first()


def make_call_by_user(user_id: int):
    """
    Make a new call by user or set to null old call
    :param user_id: User's Telegram-ID
    :return: void
    """
    current_call = _get_current_user_call(user_id)
    if not current_call:
        user = userservice.get_user_by_id(user_id)
        new_call = Call()
        user.calls.append(new_call)
        db.session.add(user)
    db.session.commit()


def set_call_phone_number(user_id: int, phone_number: str):
    """
    Set phone number to current user's order to call
    :param user_id: User's Telegram-ID
    :param phone_number: user's phone number
    :return: void
    """
    current_call = _get_current_user_call(user_id)
    current_call.phone_number = phone_number
    db.session.commit()


def set_call_time(user_id: int, time: str):
    """
    Set time to current user's order to call
    :param user_id: User's Telegram-ID
    :param time: Time, when the call must be made
    :return: void
    """
    current_call = _get_current_user_call(user_id)
    current_call.time = time
    db.session.commit()


def confirm_call_order(user_id):
    """
    Confirm the user's current call order
    :param user_id: User's Telegram-ID
    :return: void
    """
    current_call = _get_current_user_call(user_id)
    current_call.confirmed = True
    current_call.confirmation_date = datetime.utcnow()
    db.session.commit()


def get_all_confirmed_calls() -> list:
    """
    Get all confirmed calls
    :return: list of application.core.models.Call
    """
    return Call.query\
        .filter(Call.confirmed == True)\
        .order_by(Call.confirmation_date.desc())\
        .all()


def remove_call(call_id: int):
    """
    Delete call by its id
    :param call_id: Call's id
    :return: void
    """
    call = Call.query.get_or_404(call_id)
    db.session.delete(call)
    db.session.commit()
