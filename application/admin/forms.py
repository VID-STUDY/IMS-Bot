from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, MultipleFileField, ValidationError
from wtforms.validators import DataRequired
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

    def validate_name(self, name: StringField):
        if TVChannel.query.filter(TVChannel.name == name.data).count() > 0:
            raise ValidationError('Канал с таким именем уже существует')
