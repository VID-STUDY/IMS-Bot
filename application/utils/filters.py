from application import app
from .tools import convert_utc_to_asia


@app.template_filter
def datetime(value, date_format='%d.%m.%Y %H:%M:%S'):
    return convert_utc_to_asia(value).strftime(date_format)
