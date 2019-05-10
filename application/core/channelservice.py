from application import db
from application.core.models import TVChannel, PriceFile, ChannelPresentation
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
        if not price_files[0].content_type == 'application/octet-stream':
            current_prices = channel.price_files.filter(PriceFile.is_package == False).all()
            for price_file in current_prices:
                db.session.delete(price_file)
                tools.remove_file(price_file.file_path)
            for file in price_files:
                if file.filename == '':
                    continue
                file_path = os.path.join(Config.UPLOAD_DIRECTORY, secure_filename(file.filename))
                tools.save_file(file, file_path, recreate=True)
                new_price = PriceFile(file_path=file_path, is_package=False)
                channel.price_files.append(new_price)
                db.session.add(new_price)
    if package_offers_files:
        if not package_offers_files[0].content_type == 'application/octet-stream':
            current_package_offers = channel.price_files.filter(PriceFile.is_package == True).all()
            for offer in current_package_offers:
                db.session.delete(offer)
                tools.remove_file(offer.file_path)
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
            channel.price_files.append(new_package_offer)
            db.session.add(new_package_offer)
    db.session.commit()


def remove_channel(channel_id: int):
    """
    Remove channel
    :param channel_id: Channel's ID
    :return: void
    """
    channel = TVChannel.query.get_or_404(channel_id)
    for file in channel.price_files.all():
        tools.remove_file(file.file_path)
    db.session.delete(channel)
    db.session.commit()


def get_channel_presentations():
    """
    All channles' presentations
    :return: list of presentations models
    """
    return ChannelPresentation.query.all()


def set_telegram_id_for_presentation_file(presentation_id, telegram_id):
    """
    Setting up a Telegram-ID for file
    :param presentation_id: file id
    :param telegram_id: Telegram-ID
    :return: void
    """
    presentation = ChannelPresentation.query.get(presentation_id)
    presentation.telegram_id = telegram_id
    db.session.commit()


def update_presentations(files):
    """
    Delete all old files and save new presntantions files
    :param files: a list of FileStorage
    :return: void
    """
    if files:
        if not files[0].content_type == 'application/octet-stream':
            current_presentations = get_channel_presentations()
            for file in current_presentations:
                tools.remove_file(file.file_path)
            ChannelPresentation.query.delete()
            for file in files:
                if file.filename == '':
                    continue
                file_path = os.path.join(Config.UPLOAD_DIRECTORY, secure_filename(file.filename))
                tools.save_file(file, file_path, recreate=True)
                new_presentation = ChannelPresentation(file_path=file_path)
                db.session.add(new_presentation)
            db.session.commit()


class ChannelNotFound(Exception):
    pass
