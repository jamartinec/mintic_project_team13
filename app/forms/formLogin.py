from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

# Clase del formulario, se agrega las validaciones
class FormLogin(FlaskForm):
    user = StringField("Usuario", validators = [DataRequired(message = 'Campo usuario requerido'), Length(min = 8, max = 10 ,message="El usuario debe tener minimo 8 caracteres y maximo 10")])
    password = PasswordField("Contraseña", validators = [DataRequired(message = 'Campo Contraseña requerido'), Length(min = 8, max = 15 ,message="La contraseña debe tener minimo 8 caracteres y maximo 15")])
    remember = BooleanField("Recordar usuario")
    sendForm = SubmitField("Iniciar sesión")

