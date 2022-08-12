from flask import request, Flask, flash, render_template, jsonify, url_for, session, make_response, g, redirect
from forms.formLogin import FormLogin
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
    data = {
        'title': 'Inicio',
        'description': "Hotel Mintic Ciclo 3 NCR 1873"
    }
    session['usuario'] = "Brayan"   
    visited = request.cookies.get("visited")
    if visited == 'True':
        return render_template("index.html", data = data)
    else:
        response = make_response(render_template(
            'index.html', data = data))
        return response

# Ruta para el login del usuario
@app.route('/iniciarSesion', methods=["GET", "POST"])
def login():
    data = {
        'title': 'Iniciar Sesion',
        'description': "Hotel Mintic Ciclo 3 NCR 1873",
        'form': FormLogin()
    }
    return render_template('iniciarSesion.html', data=data)

# Ruta para el registro del usuario 


@app.route('/registrar', methods=["GET", "POST"])
def register():
    data = {
        'title': 'Registrar Usuario',
        'description': "Hotel Mintic Ciclo 3 NCR 1873",
        'form': FormLogin()
    }
    return render_template('crearUsuario.html', data=data)

@app.route('/editarReserva')
def getProductos():
    lista_reservas = bd.sql_select_reserva()
    flash("Lista de reservas")
    return render_template('editarReserva.html',l_reservas=lista_reservas,titulo="Lista de reservas")



# Función para validar cuando no es una ruta válida y se redirecciona al index


def pageNoFound(error):
    data = {
        'title': 'Página no encontrada',
        'description': "Página no encontrada"
    }
    # return render_template('404.html', data = data), 404
    return redirect(url_for('index'))

@app.route('/cerrar')
def cerrar():
    flash("Sesion cerrada")
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.register_error_handler(404, pageNoFound)
    app.run(debug=True, port=5000)
