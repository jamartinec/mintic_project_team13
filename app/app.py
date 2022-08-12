from flask import Flask, render_template, url_for, redirect, request
from forms.formLogin import FormLogin
from settings.config import Configuration

app = Flask(__name__)

app.config.from_object(Configuration)

# Ruta principal, inicio de la aplicación
@app.route('/')
def index():
    data = {
        'title': 'Inicio',
        'description': "Hotel Mintic Ciclo 3 NCR 1873"
    }
    return render_template('index.html', data = data)

# Ruta para el login del usuario
@app.route('/iniciarSesion')
def login():
    data = {
        'title': 'Iniciar Sesion',
        'description': "Hotel Mintic Ciclo 3 NCR 1873",
        'form': FormLogin()
    }
    return render_template('iniciarSesion.html', data = data)

    # Ruta para el registro del usuario
@app.route('/registrar')
def register():
    data = {
        'title': 'Registrar Usuario',
        'description': "Hotel Mintic Ciclo 3 NCR 1873",
        'form': FormLogin()
    }
    return render_template('crearUsuario.html', data = data)

# Función para validar cuando no es una ruta válida y se redirecciona al index
def pageNoFound(error):
    data = {
        'title': 'Página no encontrada',
        'description': "Página no encontrada"
    }
    # return render_template('404.html', data = data), 404
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.register_error_handler(404, pageNoFound)
    app.run(debug=True, port=5000)
