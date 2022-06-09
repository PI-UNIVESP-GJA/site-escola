from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class FormLogin(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    senha = PasswordField('senha', validators=[DataRequired()])
    manterConectado = BooleanField('manterConectado')

class FormCadastro(FlaskForm):
    nome = StringField('email', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    senha = PasswordField('senha', validators=[DataRequired()])
    confirmar_senha = PasswordField('senha', validators=[DataRequired()])

class FormCadastroAluno(FlaskForm):
    numero = StringField('numero', validators=[DataRequired()])
    nome = StringField('nome', validators=[DataRequired()])
    classe = StringField('classe', validators=[DataRequired()])
    materia = StringField('materia', validators=[DataRequired()])
    nota = StringField('nota', validators=[DataRequired()])
    aulas = StringField('aulas', validators=[DataRequired()])
    faltas = StringField('faltas', validators=[DataRequired()])

class FormAtualizaAluno(FlaskForm):
    numero = StringField('numero')
    nome = StringField('nome')
    classe = StringField('classe')
    materia = StringField('materia')
    nota = StringField('nota')
    aulas = StringField('aulas')
    faltas = StringField('faltas')

class FormConsultaAluno(FlaskForm):
    numero = StringField('numero')
    nome = StringField('nome')
    classe = StringField('classe')
    materia = StringField('materia')
    nota = StringField('nota')
    aulas = StringField('aulas')
    faltas = StringField('faltas')