from application import app
from application.resources.strings import from_target_audience_enum_to_text, format_ages, budget_enum_to_text
from .tools import convert_utc_to_asia


@app.template_filter()
def datetime(value, date_format='%d.%m.%Y %H:%M:%S', convert_from_utc=False):
    if convert_from_utc:
        date = convert_utc_to_asia(value)
    else:
        date = value
    return date.strftime(date_format)


@app.template_filter()
def target_audience(value):
    return from_target_audience_enum_to_text(value, 'ru')


@app.template_filter()
def audience_age(value):
    return format_ages(value, 'ru')



@app.template_filter()
def budget(value):
    return budget_enum_to_text(value, 'ru')
