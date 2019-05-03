from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, MultipleFileField, ValidationError
from wtforms.validators import DataRequired
from application.core.models import TVChannel


class ChannelForm(FlaskForm):
    name = StringField('Название канала', validators=[DataRequired('Имя обзательно')])
    price_files = MultipleFileField('Файлы прайсов')
    package_offers_files = MultipleFileField('Файлы пакетных предложений')
    submit = SubmitField('Сохранить')

    def validate_name(self, name: StringField):
        if TVChannel.query.filter(TVChannel.name == name.data).count() > 0:
            raise ValidationError('Канал с таким именем уже существует')
