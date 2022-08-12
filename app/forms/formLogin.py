from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

# Clase del formulario, se agrega las validaciones
class FormLogin(FlaskForm):
    user = StringField("Usuario", validators = [DataRequired(message = 'Campo requerido'), Length(min = 8, max = 10 ,message="El usuario debe tener minimo 8 caracteres y maximo 10")])
    password = PasswordField("Contraseña", validators = [DataRequired(message = 'Ingrese contraseña')])
    remember = BooleanField("Recordar usuario")
    sendForm = SubmitField("Iniciar sesión")

class FormLReservar(FlaskForm):
    search = StringField("Buscar", validators = [DataRequired(message = 'Campo requerido') ])
