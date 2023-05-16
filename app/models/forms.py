from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class FormLogin(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    senha = PasswordField('senha', validators=[DataRequired()])
    manterConectado = BooleanField('manterConectado')