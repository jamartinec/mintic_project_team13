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

listRoom = []

# @app.before_request
# def before_request():
#     listRoom = db.sql_consultar_habitaciones()
#     print("listRoom: ", listRoom[0][5])


# Ruta principal, inicio de la aplicación


@app.route('/')
def index():
    listRoom = db.sql_consultar_habitaciones()
    visited = request.cookies.get("visited")
    formulario = FormReserve()
    # listRoom = [["101", "Habitación Especial", "5", "https://i.pinimg.com/originals/4d/2a/c6/4d2ac66204416672fcc444b2bf2e6ac6.jpg"], ["102", "Habitación Sencilla", "3.5", "https://3.bp.blogspot.com/-0TJZXFkn1jo/XHoG0-VpbKI/AAAAAAAADFc/GMkvLd_D6Dkbl6nJy5u6JgSsCdj5mknBgCLcBGAs/s640/Asian%252Binspired%252Bluxurious%252Bbedroom.jpg"], ["103", "Habitación Sencilla", "4", "https://casaydiseno.com/wp-content/uploads/2020/09/habitacion-suite-ideas-diseno-chimenea.jpg"],
    #             ["104", "Habitación Matrimonial", "5", "http://2.bp.blogspot.com/-gW8qrVLtUhE/URm12WBuQfI/AAAAAAAAig8/4BsvHqf8PDg/s1600/dormitorio-paredes-chocolate.jpg"], ["105", "Habitación Sencilla", "5", "https://www.guiaparadecorar.com/wp-content/uploads/2016/02/12-impresionantes-y-lujosas-habitaciones-de-hotel-04-e1456292481895.jpg"], ["106", "Habitación Sencilla", "3.9", "https://casaydiseno.com/wp-content/uploads/2015/03/cama-grande-techo-l%C3%A1mpara.jpg"]]
    if visited == 'True':
        data = {
            'title': 'Reservar Habitación',
            'description': "Hotel Mintic Ciclo 3 NCR 1873",
            'listRoom': listRoom
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

    listRoom = db.sql_consultar_habitaciones()
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
    formularioReserve = FormReserve()
    if request.method == 'GET':
        return render_template('iniciarSesion.html', data=data, form=formulario)

    if request.method == 'POST':
        if formulario.validate_on_submit():

            user = request.form.get("user")
            password = request.form.get("password")
            remember = formulario.remember.data

            print("remember: ", remember)

            userInfo = db.sql_consultar_usuario(user)

            if userInfo is not None:
                passwordHash = userInfo[2]
                if check_password_hash(passwordHash, password):
                    flash(f'Usuario {userInfo[1]} logueado correctamente!')
                    session['usuario'] = userInfo[1]
                    response = make_response(render_template(
                        'reservarHabitacion.html', data=data, form=formularioReserve))
                    response.set_cookie('visited', 'True')

                    if remember:
                        print("remember if: ", remember)
                        response.set_cookie('user', session['usuario'])
                        response.set_cookie('remember', 'True')
                    else:
                        print("remember else: ", remember)
                        response.set_cookie('user', "")
                        response.set_cookie('remember', 'False')
                    return response
            else:
                flash(f'Usuario o contraseña incorrecta!')
        return render_template('iniciarSesion.html', data=data, form=formulario)


# Ruta para reservar habitación del usuario
@app.route('/reserveRoom', methods=["GET", "POST"])
def reserveRoom():
    listRoom = db.sql_consultar_habitaciones()
    # listRoom = [["101", "Habitación Especial", "5", "https://i.pinimg.com/originals/4d/2a/c6/4d2ac66204416672fcc444b2bf2e6ac6.jpg"], ["102", "Habitación Sencilla", "3.5", "https://3.bp.blogspot.com/-0TJZXFkn1jo/XHoG0-VpbKI/AAAAAAAADFc/GMkvLd_D6Dkbl6nJy5u6JgSsCdj5mknBgCLcBGAs/s640/Asian%252Binspired%252Bluxurious%252Bbedroom.jpg"], ["103", "Habitación Sencilla", "4", "https://casaydiseno.com/wp-content/uploads/2020/09/habitacion-suite-ideas-diseno-chimenea.jpg"],
    #             ["104", "Habitación Matrimonial", "5", "http://2.bp.blogspot.com/-gW8qrVLtUhE/URm12WBuQfI/AAAAAAAAig8/4BsvHqf8PDg/s1600/dormitorio-paredes-chocolate.jpg"], ["105", "Habitación Sencilla", "5", "https://www.guiaparadecorar.com/wp-content/uploads/2016/02/12-impresionantes-y-lujosas-habitaciones-de-hotel-04-e1456292481895.jpg"], ["106", "Habitación Sencilla", "3.9", "https://casaydiseno.com/wp-content/uploads/2015/03/cama-grande-techo-l%C3%A1mpara.jpg"]]
    formulario = FormReserve()
    data = {
        'title': 'Reservar Habitación',
        'description': "Hotel Mintic Ciclo 3 NCR 1873",
        'listRoom': listRoom
    }
    return render_template('reservarHabitacion.html', data=data, form=formulario)

# Ruta para el registro del usuario


@app.route('/registrar', methods=["GET", "POST"])
def register():

    data = {
        'title': 'Iniciar Sesion',
        'description': "Hotel Mintic Ciclo 3 NCR 1873"
    }

    formulario = FormRegister()

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

            if db.sql_existe_usuario(user, email) > 0:
                flash(f'Usuario {user} ya existe!')
            else:
                last_row_id = db.sql_insert_user(
                    user, datetime.now(), name, email, document, contact, 3)
                db.sql_insert_contrasena(last_row_id, user, passwordHash)
                flash(f'Usuario {name} registrado con exito!')
                return redirect(url_for('index'))
        return render_template('crearUsuario.html', data=data, form=formulario)

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
    listRoom = db.sql_consultar_habitaciones()
    # listRoom = [["101", "Habitación Especial", "5", "https://i.pinimg.com/originals/4d/2a/c6/4d2ac66204416672fcc444b2bf2e6ac6.jpg"], ["102", "Habitación Sencilla", "3.5", "https://3.bp.blogspot.com/-0TJZXFkn1jo/XHoG0-VpbKI/AAAAAAAADFc/GMkvLd_D6Dkbl6nJy5u6JgSsCdj5mknBgCLcBGAs/s640/Asian%252Binspired%252Bluxurious%252Bbedroom.jpg"], ["103", "Habitación Sencilla", "4", "https://casaydiseno.com/wp-content/uploads/2020/09/habitacion-suite-ideas-diseno-chimenea.jpg"],
    #             ["104", "Habitación Matrimonial", "5", "http://2.bp.blogspot.com/-gW8qrVLtUhE/URm12WBuQfI/AAAAAAAAig8/4BsvHqf8PDg/s1600/dormitorio-paredes-chocolate.jpg"], ["105", "Habitación Sencilla", "5", "https://www.guiaparadecorar.com/wp-content/uploads/2016/02/12-impresionantes-y-lujosas-habitaciones-de-hotel-04-e1456292481895.jpg"], ["106", "Habitación Sencilla", "3.9", "https://casaydiseno.com/wp-content/uploads/2015/03/cama-grande-techo-l%C3%A1mpara.jpg"]]
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
