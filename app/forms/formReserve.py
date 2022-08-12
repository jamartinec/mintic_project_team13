from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo 

# Clase del formulario, se agrega las validaciones


class FormReserve(FlaskForm):
    dateIni = StringField("Fecha de ingreso", validators=[DataRequired(message='Campo nombre requerido')])
    dateFin = StringField("Fecha de salida", validators=[DataRequired(message='Campo usuario requerido')])
    cantPerson = StringField("Cantidad de personas", validators=[DataRequired(message='Campo Contraseña requerido')])
    reserveForm = SubmitField("Reservar")