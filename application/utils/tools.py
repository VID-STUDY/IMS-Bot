from datetime import datetime
from dateutil import tz
import os


def convert_utc_to_asia(utc_date: datetime):
    from_zone = tz.tzutc()
    to_zone = tz.gettz('Asia/Tashkent')
    utc = utc_date.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)
    return local


def save_file(file, path, recreate=False):
    """
    Save file to path
    :param file: File
    :param path: Path
    :param recreate: If file exists remove old version, save new version
    :return: void
    """
    if os.path.exists(path):
        if recreate:
            os.remove(path)
        else:
            raise FileExistsError()
    file.save(path)


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
