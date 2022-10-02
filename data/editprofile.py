from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField


class EditProfileForm(FlaskForm):
    surname = StringField('Фамилия')
    name = StringField('Имя')
    speciality = StringField('Специализация')
    old_password = PasswordField('Старый пароль')
    new_password = PasswordField('Новый пароль')
    submit = SubmitField('Подтвердить')
