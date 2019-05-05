from application import app
from .tools import convert_utc_to_asia


@app.template_filter()
def datetime(value, date_format='%d.%m.%Y %H:%M:%S', convert_from_utc=False):
    if convert_from_utc:
        date = convert_utc_to_asia(value)
    else:
        date = value
    return date.strftime(date_format)
