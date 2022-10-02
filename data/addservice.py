from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SubmitField, StringField, TextAreaField, FloatField, SelectField, FileField
from wtforms.validators import DataRequired
from data.givebranches import bran


class AddServiceForm(FlaskForm):
    service = StringField('Услуга', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    branch = SelectField('Выберите категорию', choices=bran(), validators=[DataRequired()])
    price = FloatField('Цена', validators=[DataRequired()])
    preview = FileField('Предпросмотр (Изображение в формате jpg/png)',
                        validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Подтвердить')
