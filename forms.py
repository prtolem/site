from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class Login(FlaskForm):
    name = StringField("Логин :", validators=[DataRequired(),Length(min=4,max=25)])
    password = PasswordField("Пароль",validators=[DataRequired()])
    submit = SubmitField("Авторизоваться")

class Participation(FlaskForm):
    cookies = StringField("Куки :", validators=[DataRequired()])
    proxy = StringField("Прокси :")
    UserAgent = StringField("Юзер-агент :")
    submit = SubmitField('Отправить')
