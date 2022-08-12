from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email 

# Clase del formulario, se agrega las validaciones


class FormRegister(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired(message='Campo nombre requerido'), Length(
        min=8, max=30, message="El usuario debe tener minimo 8 caracteres y maximo 30")])
    user = StringField("Usuario", validators=[DataRequired(message='Campo usuario requerido'), Length(
        min=8, max=10, message="El usuario debe tener minimo 8 caracteres y maximo 10")])
    password = PasswordField("Contraseña", validators=[DataRequired(message='Campo Contraseña requerido'), Length(
        min=8, max=15, message="La contraseña debe tener minimo 8 caracteres y maximo 15"), EqualTo('confPassword', message='Las contraseñas no son iguales')])
    confPassword = PasswordField("Confirmar contraseña", validators=[DataRequired(message='Confirmar Contraseña requerido'), Length(
        min=8, max=15, message="La contraseña debe tener minimo 8 caracteres y maximo 15")])
    email = EmailField("Correo", validators=[DataRequired(message='Campo correo requerido'), Length(
        min=8, max=50, message="El correo debe tener minimo 8 caracteres y maximo 50"), EqualTo('ConfEmail', message='Los correos no son iguales'), Email(message="Correo no válido") ])
    ConfEmail = EmailField("Confirmar correo", validators=[DataRequired(message='Confirmar correo requerido'), Length(
        min=8, max=50, message="El correo debe tener minimo 8 caracteres y maximo 50"), Email(message="Correo no válido")])
    registerForm = SubmitField("Registrar")
