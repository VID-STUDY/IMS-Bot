from application import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model):
    """
    Model for users in bot
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    language = db.Column(db.String(5))
    company_name = db.Column(db.String(100))
    registered_at = db.Column(db.DateTime)
    calls = db.relationship('Call', lazy='dynamic', backref='user')
    campaigns = db.relationship('AdCampaign', lazy='dynamic', backref='user')


class AdminUser(db.Model, UserMixin):
    """
    Model for users in administration panel
    """
    __tablename__ = 'admin_users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True)
    password_hash = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Call(db.Model):
    """
    Model for call orders
    """
    __tablename__ = 'calls'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15))
    time = db.Column(db.String(50))
    confirmed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    confirmation_date = db.Column(db.DateTime)


class TVChannel(db.Model):
    """
    Model for TV channels
    """
    __tablename__ = 'tv_channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price_files = db.relationship('PriceFile', lazy='dynamic', cascade='all,delete')


class PriceFile(db.Model):
    """
    Model for prices in files
    """
    __tablename__ = 'price_files'
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(150))
    file_path = db.Column(db.String(150))
    channel_id = db.Column(db.Integer, db.ForeignKey('tv_channels.id'))
    is_package = db.Column(db.Boolean, default=False)


class AdCampaign(db.Model):
    """
    Model for advertising campaigns
    """
    __tablename__ = 'ad_campaigns'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150))
    target_audience = db.Column(db.String(50))
    age_of_audience = db.Column(db.String(100))
    budget = db.Column(db.String(50))
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    class TargetAudiences:
        MALE = 'male'
        FEMALE = 'female'
        MALE_AND_FEMALE = 'male_and_female'

    class BudgetOptions:
        SMALL = "small"
        MEDIUM = "medium"
        LARGE = 'large'
        VERY_LARGE = 'very_large'

    class AudienceAges:
        AGES = ['6-10', '11-17', '18-24', '25-34', '35-44', '45-54', '55_and_older']
        ALL = 'all'


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_ru = db.Column(db.String(6000))
    text_uz = db.Column(db.String(6000))


class ChannelPresentation(db.Model):
    __tablename__ = 'channel_presentations'
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(150))
    file_path = db.Column(db.String(150))


class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_ru = db.Column(db.String(6000))
    text_uz = db.Column(db.String(6000))


class NotifyChat(db.Model):
    __tablename__ = 'notify_chats'
    id = db.Column(db.Integer, primary_key=True)
    chat_title = db.Column(db.String(100))


@login.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))
