from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FloatField, SelectField, BooleanField, FileField
from flask_wtf.file import FileAllowed
from data.givebranches import bran


class EditServiceForm(FlaskForm):
    service = StringField('Услуга')
    description = TextAreaField('Описание')
    branch = SelectField('Выберите категорию', choices=bran())
    price = FloatField('Цена')
    preview = FileField('Предпросмотр (Изображение в формате jpg/png)',
                        validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    action = BooleanField('Активно', default=True)
    submit = SubmitField('Подтвердить')
