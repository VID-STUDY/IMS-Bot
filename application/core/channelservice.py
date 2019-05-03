from application import db
from application.core.models import TVChannel, PriceFile


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
    return tv_channel.price_files.all()


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


class ChannelNotFound(Exception):
    pass
