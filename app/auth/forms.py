from flask_wtf import FlaskForm
from wtforms import validators, SubmitField, StringField, PasswordField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[Required()])
    password = PasswordField('密码', validators=[Required()])
    submit = SubmitField('登录')