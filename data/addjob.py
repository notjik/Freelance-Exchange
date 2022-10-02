from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SubmitField, StringField, TextAreaField, FloatField, FileField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Вакансия', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    price = FloatField('Цена', validators=[DataRequired()])
    preview = FileField('Предпросмотр (Изображение в формате jpg/png)',
                        validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Подтвердить')
