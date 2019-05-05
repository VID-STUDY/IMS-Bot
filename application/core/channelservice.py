from application import db
from application.core.models import TVChannel, PriceFile
from config import Config
from application.utils import tools
from werkzeug.utils import secure_filename
import os


def get_all_channels() -> list:
    """
    Get all channels
    :return: List of channels
    """
    return TVChannel.query.all()


def get_prices_by_channel(name: str) -> list:
    """
    Get prices by concrete channel
    :param name: Channel name
    :return: list of application.core.models.PriceFile
    """
    tv_channel = TVChannel.query.filter(TVChannel.name == name).first()
    if not tv_channel:
        raise ChannelNotFound()
    return tv_channel.price_files.filter(PriceFile.is_package == False).all()


def set_telegram_id_for_price_file(price_file_id: int, telegram_id: str):
    """
    Set file's telegram id for sending files quickly
    :param price_file_id: Id of price file in database
    :param telegram_id: Id of file in the Telegram server
    :return: void
    """
    price_file = PriceFile.query.get(price_file_id)
    price_file.telegram_id = telegram_id
    db.session.commit()


def get_package_offers_by_channel(name: str) -> list:
    """
    Get package offers by concrete channel
    :param name: Channel's name
    :return: list of application.core.models.PriceFile
    """
    tv_channel = TVChannel.query.filter(TVChannel.name == name).first()
    if not tv_channel:
        raise ChannelNotFound()
    return tv_channel.price_files.filter(PriceFile.is_package == True).all()


def get_channels_only_with_package_offers() -> list:
    """
    Return channels that have at least one package offer
    :return: list of application.core.models.TvChannel
    """
    tv_channels = TVChannel.query.all()
    sorted_channels = []
    for channel in tv_channels:
        if channel.price_files.filter(PriceFile.is_package == True).count() > 0:
            sorted_channels.append(channel)
    return sorted_channels


def get_channels_only_with_price_files() -> list:
    """
    Return channels that have at least one price
    :return: list of application.core.models.TvChannel
    """
    tv_channels = TVChannel.query.all()
    sorted_channels = []
    for channel in tv_channels:
        if channel.price_files.filter(PriceFile.is_package == False).count() > 0:
            sorted_channels.append(channel)
    return sorted_channels


def get_channel_by_id(channel_id: int) -> TVChannel:
    """
    Get channel by id or abort with 404
    :param channel_id: Channel's ID
    :return: application.core.models.TvChannel
    """
    return TVChannel.query.get_or_404(channel_id)


def update_channel(channel_id: int, name=None, price_files=None, package_offers_files=None):
    """
    Update a channel. Remove old price and package offers files and recreate them with new
    :param channel_id: Channel's ID
    :param name: new channel's name
    :param price_files: new channel's prices
    :param package_offers_files: new channel's package offers
    :return: void
    """
    channel = get_channel_by_id(channel_id)
    if name:
        channel.name = name
    if price_files:
        current_prices = channel.price_files.filter(PriceFile.is_package == False).all()
        map(db.session.delete, current_prices)
        for file in price_files:
            if file.filename == '':
                continue
            file_path = os.path.join(Config.UPLOAD_DIRECTORY, secure_filename(file.filename))
            tools.save_file(file, file_path, recreate=True)
            new_price = PriceFile(file_path=file_path, is_package=False)
            channel.price_files.append(new_price)
            db.session.add(new_price)
    if package_offers_files:
        current_package_offers = channel.price_files.filter(PriceFile.is_package == True).all()
        map(db.session.delete, current_package_offers)
        for file in package_offers_files:
            if file.filename == '':
                continue
            file_path = os.path.join(Config.UPLOAD_DIRECTORY, secure_filename(file.filename))
            tools.save_file(file, file_path, recreate=True)
            new_package_offer = PriceFile(file_path=file_path, is_package=True)
            channel.price_files.append(new_package_offer)
            db.session.add(new_package_offer)
    db.session.commit()


def create_channel(name: str, price_files=None, package_offers_files=None):
    """
    Create a new channel
    :param name: Channel name
    :param price_files: Paths of price files
    :param package_offers_files: Paths of package offers files
    :return: void
    """
    channel = TVChannel(name=name)
    db.session.add(channel)
    if price_files:
        for file in price_files:
            if file.filename == '':
                continue
            file_path = os.path.join(Config.UPLOAD_DIRECTORY, secure_filename(file.filename))
            tools.save_file(file, file_path, recreate=True)
            new_price = PriceFile(file_path=file_path, is_package=False)
            channel.price_files.append(new_price)
            db.session.add(new_price)
    if package_offers_files:
        for file in package_offers_files:
            if file.filename == '':
                continue
            file_path = os.path.join(Config.UPLOAD_DIRECTORY, secure_filename(file.filename))
            tools.save_file(file, file_path, recreate=True)
            new_package_offer = PriceFile(file_path=file_path, is_package=True)
            channel.price_files.add(new_package_offer)
            db.session.add(new_package_offer)
    db.session.commit()


def remove_channel(channel_id: int):
    """
    Remove channel
    :param channel_id: Channel's ID
    :return: void
    """
    channel = TVChannel.query.get_or_404(channel_id)
    db.session.delete(channel)
    db.session.commit()


class ChannelNotFound(Exception):
    pass
