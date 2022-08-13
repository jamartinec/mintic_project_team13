from flask import request, Flask, flash, render_template, jsonify, url_for, session, make_response, g, redirect
from forms.formLogin import FormLogin
from forms.formRegister import FormRegister
from forms.formReserve import FormReserve
from settings.config import Configuration
import database as db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config.from_object(Configuration)

listUsers = []
listTypeUser = []
listRoom = []


@app.before_request
def before_request():
    getListRooms()
    getUser()
    getTypeUser()


def getUser():
    global listUsers
    listUsers = db.sql_consultar_usuarios()
    if len(listUsers) == 0:
        passwordHash = generate_password_hash("SuperAdmin", method='sha256')
        last_row_id = db.sql_insert_user("SuperAdmin", datetime.now(
        ), "SuperAdmin", "soporte@hotel.com", "123456789", "123456789", 1)
        db.sql_insert_contrasena(last_row_id, "SuperAdmin", passwordHash)


def getTypeUser():
    global listTypeUser
    listTypeUser = db.sql_consultar_type_usuarios()


def getListRooms():
    global listRoom
    listRoom = db.sql_consultar_habitaciones()

# Ruta principal, inicio de la aplicación


@app.route('/')
def index():
    global listRoom
    visited = request.cookies.get("visited")
    formulario = FormReserve()
    if visited == 'True':
        data = {
            'title': 'Reservar Habitación',
            'description': "Hotel Mintic Ciclo 3 NCR 1873",
            'listRoom': listRoom,
            'listTypeUser': listTypeUser
        }
        return render_template("reservarHabitacion.html", data=data, form=formulario)
    else:
        data = {
            'title': 'Inicio',
            'description': "Hotel Mintic Ciclo 3 NCR 1873",
            'listRoom': listRoom
        }
        return render_template('index.html', data=data)

# Ruta para el login del usuario


@app.route('/iniciarSesion', methods=["GET", "POST"])
def login():

    global listRoom
    if request.cookies.get("remember") == 'True':
        checkRemember = True
    else:
        checkRemember = False

    data = {
        'title': 'Reservar Habitación',
        'description': "Hotel Mintic Ciclo 3 NCR 1873",
        'listRoom': listRoom,
        'checkRemember': checkRemember,
        'userRemember': request.cookies.get("user")
    }
    formulario = FormLogin()

    if request.method == 'GET':
        return render_template('iniciarSesion.html', data=data, form=formulario)

    if request.method == 'POST':
        if formulario.validate_on_submit():

            user = request.form.get("user")
            password = request.form.get("password")
            remember = formulario.remember.data

            userInfoLogin = db.sql_consultar_usuario(user)

            if userInfoLogin is not None:
                userInfo = db.sql_consultar_usuario_name(user)
                passwordHash = userInfoLogin[2]
                if check_password_hash(passwordHash, password):
                    session['usuario'] = userInfo[1]
                    session['user_id'] = userInfo[0]
                    session['type_user'] = userInfo[7]
                    response = make_response(redirect(url_for('reserveRoom')))
                    response.set_cookie('visited', 'True')
                    flash(f'Usuario {userInfo[1]} logueado correctamente!')
                    if remember:
                        response.set_cookie('user', session['usuario'])
                        response.set_cookie('remember', 'True')
                    else:
                        response.set_cookie('user', "")
                        response.set_cookie('remember', 'False')
                    return response
                else:
                    flash(f'Usuario o contraseña incorrecta!')
            else:
                flash(f'Usuario no encontrado!')
                return redirect(url_for('register'))
        return render_template('iniciarSesion.html', data=data, form=formulario)


# Ruta para reservar habitación del usuario
@app.route('/reserveRoom', methods=["GET", "POST"])
def reserveRoom():
    global listRoom
    formulario = FormReserve()
    data = {
        'title': 'Reservar Habitación',
        'description': "Hotel Mintic Ciclo 3 NCR 1873",
        'listRoom': listRoom
    }

    if request.method == 'GET':
        return render_template('reservarHabitacion.html', data=data, form=formulario)

    if request.method == 'POST':
        return render_template('reservarHabitacion.html', data=data, form=formulario)

# Ruta para el registro del usuario


@app.route('/registrar', methods=["GET", "POST"])
def register():

    data = {
        'title': 'Iniciar Sesion',
        'description': "Hotel Mintic Ciclo 3 NCR 1873"
    }

    formulario = FormRegister()
    formularioLogin = FormLogin()

    if request.method == 'GET':
        return render_template('crearUsuario.html', data=data, form=formulario)

    if request.method == 'POST':

        if formulario.validate_on_submit():
            user = request.form.get("user")
            name = request.form.get("name")
            email = request.form.get("email")
            document = request.form.get("document")
            contact = request.form.get("contact")
            passwordHash = generate_password_hash(
                request.form["password"], method='sha256')

            typeUSer = request.form.get("typeUsers")

            if typeUSer is None:
                typeUSer = 3

            if db.sql_existe_usuario(user, email) > 0:
                flash(f'Usuario {user} ya existe!')
            else:
                last_row_id = db.sql_insert_user(
                    user, datetime.now(), name, email, document, contact, typeUSer)
                db.sql_insert_contrasena(last_row_id, user, passwordHash)
                flash(f'Usuario {name} registrado con exito!')
                return render_template('iniciarSesion.html', data=data, form=formularioLogin)
        return render_template('crearUsuario.html', data=data, form=formulario)


@app.route('/buscarHabitaciones', methods=["GET", "POST"])
def getRoom():
    db.sql_consultar_habitaciones()

# Función para validar cuando no es una ruta válida y se redirecciona al index


def pageNoFound(error):
    data = {
        'title': 'Página no encontrada',
        'description': "Página no encontrada"
    }
    # return render_template('404.html', data = data), 404
    return redirect(url_for('index'))

# Función para cerra sesión


@app.route('/cerrarSesion')
def closeSesion():
    global listRoom
    data = {
        'title': 'Inicio',
        'description': "Hotel Mintic Ciclo 3 NCR 1873",
        'listRoom': listRoom
    }
    session.clear()
    flash(f'Sesion cerrada!')
    response = make_response(render_template(
        'index.html', data=data))
    response.set_cookie('visited', 'False')
    return response


if __name__ == '__main__':
    app.register_error_handler(404, pageNoFound)
    app.run(debug=True, port=5000)
