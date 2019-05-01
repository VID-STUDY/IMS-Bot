from application import db
from application.core.models import User, AdminUser


def is_user_exists(user_id: int):
    return User.query.get(user_id) is not None


def register_user(user_id: int, username: str):
    user = User(id=user_id, username=username)
    db.session.add(user)
    db.session.commit()


def set_user_name(user_id: int, user_name: str):
    user = User.query.get(user_id)
    user.name = user_name
    db.session.commit()


def set_user_phone_number(user_id: int, phone_number: str):
    user = User.query.get(user_id)
    user.phone_number = phone_number
    db.session.commit()


def set_user_language(user_id: int, language: str):
    user = User.query.get(user_id)
    user.language = language
    db.session.commit()


def set_user_company(user_id: int, company_name: str):
    user = User.query.get(user_id)
    user.company_name = company_name
    db.session.commit()


def get_user_by_id(user_id: int):
    return User.query.get(user_id)


def get_admin_user_by_email(email: str) -> AdminUser:
    return AdminUser.query.filter(AdminUser.email == email).first()


def get_admin_user_by_id(id: int) -> AdminUser:
    return AdminUser.query.get(id)


def is_user_registered(user_id):
    user = User.query.get(user_id)
    if user is None:
        return False
    return user.name is not None and user.phone_number is not None


def get_user_language(user_id: int):
    user = User.query.get(user_id)
    return user.language


def set_user_admin_password(user: AdminUser, password: str):
    user.set_password(password)
    db.session.commit()


def is_admin_user_exists(email):
    return get_admin_user_by_email(email) is not None


def get_all_bot_users():
    return User.query.all()
