from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FloatField, BooleanField, FileField
from flask_wtf.file import FileAllowed


class EditJobForm(FlaskForm):
    job = StringField('Вакансия')
    description = TextAreaField('Описание')
    price = FloatField('Цена')
    preview = FileField('Предпросмотр (Изображение в формате jpg/png)',
                        validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    action = BooleanField('Активно', default=True)
    submit = SubmitField('Подтвердить')
