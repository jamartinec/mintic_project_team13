from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange

# Clase del formulario, se agrega las validaciones


class FormReserve(FlaskForm):
    dateIni = DateField("Fecha de ingreso", validators=[DataRequired(message='Campo fecha de inicio requerido')])
    dateFin = DateField("Fecha de salida", validators=[DataRequired(message='Campo fecha de salida requerido')])
    cantPerson = IntegerField("Cantidad de personas", validators=[DataRequired(message='mínimo 1 - maximo 10 huéspedes'), NumberRange(min=1, max=10)])
    reserveForm = SubmitField("Reservar habitación")

    