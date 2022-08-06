from flask import Flask 
app = Flask(__name__)
@app.route('/index.html') 
def index():
    return '<h1>Hola!<h1>'

