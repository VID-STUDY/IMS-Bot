from application import app
from .tools import convert_utc_to_asia


@app.template_filter
def datetime(value, date_format='%d.%m.%Y %H:%M:%S', convert_from_utc=False):
    if convert_from_utc:
        date = value
    else:
        date = convert_utc_to_asia(value)
    return date.strftime(date_format)
