from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import os
import json
import base64
from functools import wraps
from Model.login import login
from Model.insert import insert_data as insert
from Model.db import get_db_connection
from Model.admin_view import admin_view_func
from Model.eliminar import eliminar_articulo
from Model.editar import editar_articulo
from Model.utils import crear_directorio_usuario
from Model.login_google import google_bp
from Model.user_view import user_view_func
from Model.editar_usuario import editar_usuario_func
from Model.detalle_articulo import detalle_articulo_func
from Model.comprar_articulo import comprar_articulo_func
from Model.admin_users_view import admin_users_view_func
from Model.historial_usuario import historial_usuario_func
from Model.carrito_usuario import carrito_usuario_func
from Model.opinion import guardar_opinion
from Model.calificar_articulo import calificar_articulo_func
from Model.finalizar_compra import finalizar_compra_func
from Model.eliminar_carrito import eliminar_carrito_func
from Model.registro import registro_func



app = Flask(__name__)

app.register_blueprint(google_bp)

app.secret_key = 'supersecretkey'  # Necesario para sesiones

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_usuario' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('Module/Login/View/login.html')

@app.route('/admin_view', methods=['GET'])
@login_required
def admin_view():
    return admin_view_func()

@app.route('/insert_view', methods=['GET'])
@login_required
def insert_view():
    return render_template('Module/InsertView/View/insert_view.html')

@app.route('/login', methods=['POST'])
def login_route():
    return login()

@app.route('/insertar', methods=['POST'])
def insertar_route():
    return insert()

@app.route('/eliminar', methods=['POST'])
def eliminar_route():
    return eliminar_articulo()

@app.route('/editar', methods=['POST'])
def editar_route():
    return editar_articulo()

@app.route('/user_view', methods=['GET'])
@login_required
def user_view():
    return user_view_func()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/editar_usuario', methods=['POST'])
@login_required
def editar_usuario():
    return editar_usuario_func()

@app.route('/articulo/<int:id_articulo>', methods=['GET'])
@login_required
def detalle_articulo(id_articulo):
    return detalle_articulo_func(id_articulo)

@app.route('/comprar_articulo/<int:id_articulo>', methods=['POST'])
@login_required
def comprar_articulo(id_articulo):
    return comprar_articulo_func(id_articulo)

@app.route('/admin_users', methods=['GET'])
@login_required
def admin_users():
    return admin_users_view_func()

@app.route('/historial', methods=['GET'])
@login_required
def historial_usuario():
    return historial_usuario_func()

@app.route('/agregar_carrito', methods=['POST'])
def agregar_carrito():
    data = request.get_json()
    id_articulo = str(data.get('id_articulo'))
    cantidad = int(data.get('cantidad', 1))
    carrito = session.get('carrito', {})
    if id_articulo in carrito:
        carrito[id_articulo] += cantidad
    else:
        carrito[id_articulo] = cantidad
    session['carrito'] = carrito
    session.modified = True
    return jsonify({'success': True})

@app.route('/carrito', methods=['GET'])
@login_required
def carrito_usuario():
    return carrito_usuario_func()

@app.route('/finalizar_compra', methods=['POST'])
@login_required
def finalizar_compra():
    return finalizar_compra_func()

@app.route('/eliminar_carrito', methods=['POST'])
@login_required
def eliminar_carrito():
    return eliminar_carrito_func()

@app.route('/calificar_articulo', methods=['POST'])
@login_required
def calificar_articulo():
    return calificar_articulo_func()

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    return registro_func()

@app.template_filter('b64encode')
def b64encode_filter(data):
    if data:
        return base64.b64encode(data).decode('utf-8')
    return ''

def crear_directorio_usuario(usuario):
    # Obtiene el escritorio del usuario
    escritorio = os.path.join(os.path.expanduser('~'), 'Desktop')
    nombre_carpeta = f"Usuario_{usuario['id_usuario']}"
    ruta_carpeta = os.path.join(escritorio, nombre_carpeta)
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
    ruta_archivo = os.path.join(ruta_carpeta, 'datos_usuario.txt')
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(json.dumps(usuario, ensure_ascii=False, indent=4))
    return ruta_archivo

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(debug=True)