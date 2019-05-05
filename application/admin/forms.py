from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, MultipleFileField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed
from application.core.models import TVChannel


class ChannelForm(FlaskForm):
    name = StringField('Название канала', validators=[DataRequired('Имя обзательно')])
    price_files = MultipleFileField('Файлы прайсов',
                                    validators=[FileAllowed(['jpg', 'png', 'pdf', 'doc', 'docx'],
                                                            message="Только файлы изображений или "
                                                                    "документов")])
    package_offers_files = MultipleFileField('Файлы пакетных предложений',
                                             validators=[FileAllowed(['jpg', 'png', 'pdf', 'doc', 'docx'],
                                                                     message="Только файлы изображений или "
                                                                             "документов")])
    submit = SubmitField('Сохранить')


class NewChannelForm(FlaskForm):
    name = StringField('Название канала', validators=[DataRequired('Имя обзательно')])
    price_files = MultipleFileField('Файлы прайсов',
                                    validators=[FileAllowed(['jpg', 'png', 'pdf', 'doc', 'docx'],
                                                            message="Только файлы изображений или "
                                                                    "документов")])
    package_offers_files = MultipleFileField('Файлы пакетных предложений',
                                             validators=[FileAllowed(['jpg', 'png', 'pdf', 'doc', 'docx'],
                                                                     message="Только файлы изображений или "
                                                                             "документов")])
    submit = SubmitField('Сохранить')

    def validate_name(self, name: StringField):
        if TVChannel.query.filter(TVChannel.name == name.data).count() > 0:
            raise ValidationError('Канал с таким именем уже существует')


class RatingForm(FlaskForm):
    date = StringField('Рейтинг за', validators=[DataRequired('Установите дату')])
    text_ru = TextAreaField('Текст на русском',
                            validators=[DataRequired('Укажите текст на русском')])
    text_uz = TextAreaField('Текст на узбекском',
                            validators=[DataRequired('Укажите текст на узбекском')])
    submit = SubmitField('Сохранить')


class FaqForm(FlaskForm):
    text_ru = TextAreaField('Текст на русском',
                            validators=[DataRequired('Укажите текст на русском')])
    text_uz = TextAreaField('Текст на узбекском',
                            validators=[DataRequired('Укажите текст на узбекском')])
    submit = SubmitField('Сохранить')
