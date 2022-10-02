from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    nickname = StringField('Имя в системе (NickName)', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия')
    name = StringField('Имя')
    speciality = StringField('Специализация')
    submit = SubmitField('Зарегестрироваться')
