from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, AnyOf

# Clase del formulario, se agrega las validaciones
class FormLogin(FlaskForm):
    user = StringField("Usuario", validators = [DataRequired(message = 'Campo usuario requerido'), Length(min = 4, max = 15 ,message="El usuario debe tener minimo 4 caracteres y maximo 15")])
    password = PasswordField("Contraseña", validators = [DataRequired(message = 'Campo Contraseña requerido'), Length(min = 4, max = 15 ,message="La contraseña debe tener minimo 4 caracteres y maximo 15")])
    remember = BooleanField("Recordar usuario", default=False, validators=[AnyOf([True, False])])
    sendForm = SubmitField("Iniciar sesión")

