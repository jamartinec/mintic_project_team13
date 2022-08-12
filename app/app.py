from flask import request, Flask, flash, render_template, jsonify, url_for, session, make_response, g, redirect
from forms.formLogin import FormLogin
from forms.formRegister import FormRegister
from forms.formReserve import FormReserve
from settings.config import Configuration
import database as bd 

app = Flask(__name__)

app.config.from_object(Configuration)


@app.before_request
def before_request():
    if 'usuario' in session:
        g.user = "Usuario logueado"
    else:
        g.user = None

# Ruta principal, inicio de la aplicación

@app.route('/')
def index():
    visited = request.cookies.get("visited")
    formulario = FormReserve()
    listRoom = [["101", "Habitación Especial", "5", "https://i.pinimg.com/originals/4d/2a/c6/4d2ac66204416672fcc444b2bf2e6ac6.jpg"], ["102", "Habitación Sencilla", "3.5", "https://3.bp.blogspot.com/-0TJZXFkn1jo/XHoG0-VpbKI/AAAAAAAADFc/GMkvLd_D6Dkbl6nJy5u6JgSsCdj5mknBgCLcBGAs/s640/Asian%252Binspired%252Bluxurious%252Bbedroom.jpg"], ["103", "Habitación Sencilla", "4", "https://casaydiseno.com/wp-content/uploads/2020/09/habitacion-suite-ideas-diseno-chimenea.jpg"],
                ["104", "Habitación Matrimonial", "5", "http://2.bp.blogspot.com/-gW8qrVLtUhE/URm12WBuQfI/AAAAAAAAig8/4BsvHqf8PDg/s1600/dormitorio-paredes-chocolate.jpg"], ["105", "Habitación Sencilla", "5", "https://www.guiaparadecorar.com/wp-content/uploads/2016/02/12-impresionantes-y-lujosas-habitaciones-de-hotel-04-e1456292481895.jpg"], ["106", "Habitación Sencilla", "3.9", "https://casaydiseno.com/wp-content/uploads/2015/03/cama-grande-techo-l%C3%A1mpara.jpg"]]
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
    listRoom = [["101", "Habitación Especial", "5", "https://i.pinimg.com/originals/4d/2a/c6/4d2ac66204416672fcc444b2bf2e6ac6.jpg"], ["102", "Habitación Sencilla", "3.5", "https://3.bp.blogspot.com/-0TJZXFkn1jo/XHoG0-VpbKI/AAAAAAAADFc/GMkvLd_D6Dkbl6nJy5u6JgSsCdj5mknBgCLcBGAs/s640/Asian%252Binspired%252Bluxurious%252Bbedroom.jpg"], ["103", "Habitación Sencilla", "4", "https://casaydiseno.com/wp-content/uploads/2020/09/habitacion-suite-ideas-diseno-chimenea.jpg"],
                ["104", "Habitación Matrimonial", "5", "http://2.bp.blogspot.com/-gW8qrVLtUhE/URm12WBuQfI/AAAAAAAAig8/4BsvHqf8PDg/s1600/dormitorio-paredes-chocolate.jpg"], ["105", "Habitación Sencilla", "5", "https://www.guiaparadecorar.com/wp-content/uploads/2016/02/12-impresionantes-y-lujosas-habitaciones-de-hotel-04-e1456292481895.jpg"], ["106", "Habitación Sencilla", "3.9", "https://casaydiseno.com/wp-content/uploads/2015/03/cama-grande-techo-l%C3%A1mpara.jpg"]]
    data = {
        'title': 'Reservar Habitación',
        'description': "Hotel Mintic Ciclo 3 NCR 1873",
        'listRoom': listRoom
    }
    formulario = FormLogin()
    formularioReserve = FormReserve()
    data = {
        'title': 'Iniciar Sesion',
        'description': "Hotel Mintic Ciclo 3 NCR 1873",
        'listRoom': listRoom
    }

    if formulario.validate_on_submit():
        flash("Se solicita iniciar sesión {}, recordar{}".format(
            formulario.user.data, formulario.remember.data))
        session['usuario'] = "Usuario Logueado"
        response = make_response(render_template(
            'reservarHabitacion.html', data=data, form=formularioReserve))
        response.set_cookie('visited', 'True')
        return response
    return render_template('iniciarSesion.html', data=data, form=formulario)


# Ruta para reservar habitación del usuario
@app.route('/reserveRoom', methods=["GET", "POST"])
def reserveRoom():
    listRoom = [["101", "Habitación Especial", "5", "https://i.pinimg.com/originals/4d/2a/c6/4d2ac66204416672fcc444b2bf2e6ac6.jpg"], ["102", "Habitación Sencilla", "3.5", "https://3.bp.blogspot.com/-0TJZXFkn1jo/XHoG0-VpbKI/AAAAAAAADFc/GMkvLd_D6Dkbl6nJy5u6JgSsCdj5mknBgCLcBGAs/s640/Asian%252Binspired%252Bluxurious%252Bbedroom.jpg"], ["103", "Habitación Sencilla", "4", "https://casaydiseno.com/wp-content/uploads/2020/09/habitacion-suite-ideas-diseno-chimenea.jpg"],
                ["104", "Habitación Matrimonial", "5", "http://2.bp.blogspot.com/-gW8qrVLtUhE/URm12WBuQfI/AAAAAAAAig8/4BsvHqf8PDg/s1600/dormitorio-paredes-chocolate.jpg"], ["105", "Habitación Sencilla", "5", "https://www.guiaparadecorar.com/wp-content/uploads/2016/02/12-impresionantes-y-lujosas-habitaciones-de-hotel-04-e1456292481895.jpg"], ["106", "Habitación Sencilla", "3.9", "https://casaydiseno.com/wp-content/uploads/2015/03/cama-grande-techo-l%C3%A1mpara.jpg"]]
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
    formulario = FormRegister()
    data = {
        'title': 'Iniciar Sesion',
        'description': "Hotel Mintic Ciclo 3 NCR 1873"
    }

    if formulario.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('crearUsuario.html', data=data, form=formulario)

@app.route('/editarReserva')
def getProductos():
    lista_reservas = bd.sql_select_reserva()
    flash("Lista de reservas")
    return render_template('editarReserva.html',l_reservas=lista_reservas,titulo="Lista de reservas")


# @app.route('/nuevo',methods=['GET', 'POST'])
# def Nuevo():
#     if request.method == 'GET':
#         form = FormLogin()
#         return render_template('nuevo.html',form=form,titulo="Registro de nuevo producto")
#     if request.method == 'POST':
#         code = request.form["codigo"]
#         nombre = request.form["nombre"]
#         precio= request.form["precio"]
#         cantidad= request.form["cantidad"]
#         bd.sql_insert_producto(code,nombre,precio,cantidad)
#         flash(f'Producto {nombre} registrado con exito!')
#         return render_template('base.html',titulo="Registro de nuevo producto")

# Ruta para editarReservaciones del Usuario

@app.route('/editarReserva', methods=["GET", "POST"])
def editBooking():
    data = {
        'title': 'EditarReserva',
        'description': "Editar Reservaciones",
        'form': FormLogin()
    }
    return render_template('editarReserva.html', data=data)

# Función para validar cuando no es una ruta válida y se redirecciona al index


def pageNoFound(error):
    data = {
        'title': 'Página no encontrada',
        'description': "Página no encontrada"
    }
    # return render_template('404.html', data = data), 404
    return redirect(url_for('index'))


@app.route('/cerrarSesion')
def closeSesion():
    listRoom = [["101", "Habitación Especial", "5", "https://i.pinimg.com/originals/4d/2a/c6/4d2ac66204416672fcc444b2bf2e6ac6.jpg"], ["102", "Habitación Sencilla", "3.5", "https://3.bp.blogspot.com/-0TJZXFkn1jo/XHoG0-VpbKI/AAAAAAAADFc/GMkvLd_D6Dkbl6nJy5u6JgSsCdj5mknBgCLcBGAs/s640/Asian%252Binspired%252Bluxurious%252Bbedroom.jpg"], ["103", "Habitación Sencilla", "4", "https://casaydiseno.com/wp-content/uploads/2020/09/habitacion-suite-ideas-diseno-chimenea.jpg"],
                ["104", "Habitación Matrimonial", "5", "http://2.bp.blogspot.com/-gW8qrVLtUhE/URm12WBuQfI/AAAAAAAAig8/4BsvHqf8PDg/s1600/dormitorio-paredes-chocolate.jpg"], ["105", "Habitación Sencilla", "5", "https://www.guiaparadecorar.com/wp-content/uploads/2016/02/12-impresionantes-y-lujosas-habitaciones-de-hotel-04-e1456292481895.jpg"], ["106", "Habitación Sencilla", "3.9", "https://casaydiseno.com/wp-content/uploads/2015/03/cama-grande-techo-l%C3%A1mpara.jpg"]]
    data = {
        'title': 'Inicio',
        'description': "Hotel Mintic Ciclo 3 NCR 1873",
        'listRoom': listRoom
    }
    flash("Sesion cerrada")
    session.clear()
    response = make_response(render_template(
        'index.html', data=data))
    response.set_cookie('visited', 'False')
    return response


if __name__ == '__main__':
    app.register_error_handler(404, pageNoFound)
    app.run(debug=True, port=5000)
