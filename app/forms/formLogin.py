from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

# Clase del formulario, se agrega las validaciones
class FormLogin(FlaskForm):
    user = StringField("Usuario", validators = [DataRequired(message = 'Ingrese usuario')])
    password = PasswordField("Contraseña", validators = [DataRequired(message = 'Ingrese contraseña')])
    remember = BooleanField("Recordar usuario")
    sendForm = SubmitField("Iniciar sesión")
