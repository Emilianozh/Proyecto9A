from Model import insert
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import subprocess
import platform
import socket
from datetime import datetime
from Model.login import login
from Model.insert import insert_data as insert
from Model.db import get_db_connection
from Model.admin_view import admin_view_func
from Model.eliminar import eliminar_articulo
from Model.editar import editar_articulo
from Model.utils import crear_directorio_usuario
import os
import json
from Model.login_google import google_bp
from Model.user_view import user_view_func
import base64
from Model.editar_usuario import editar_usuario_func
from Model.detalle_articulo import detalle_articulo_func
from Model.comprar_articulo import comprar_articulo_func
from Model.admin_users_view import admin_users_view_func
from Model.historial_usuario import historial_usuario_func
from Model.carrito_usuario import carrito_usuario_func
from flask import request, session, jsonify



app = Flask(__name__)

app.register_blueprint(google_bp)

app.secret_key = 'supersecretkey'  # Necesario para sesiones

@app.route('/')
def index():
    return render_template('Module/Login/View/login.html')

@app.route('/admin_view', methods=['GET'])
def admin_view():
    return admin_view_func()

@app.route('/insert_view', methods=['GET'])
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
def user_view():
    return user_view_func()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/editar_usuario', methods=['POST'])
def editar_usuario():
    return editar_usuario_func()

@app.route('/articulo/<int:id_articulo>', methods=['GET'])
def detalle_articulo(id_articulo):
    return detalle_articulo_func(id_articulo)

@app.route('/comprar_articulo/<int:id_articulo>', methods=['POST'])
def comprar_articulo(id_articulo):
    return comprar_articulo_func(id_articulo)

@app.route('/admin_users', methods=['GET'])
def admin_users():
    return admin_users_view_func()

@app.route('/historial', methods=['GET'])
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
def carrito_usuario():
    return carrito_usuario_func()

@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    from Model.db import get_db_connection, close_db_connection
    id_usuario = session.get('id_usuario')
    carrito = session.get('carrito', {})
    if not carrito or not id_usuario:
        return redirect('/carrito')
    connection = get_db_connection()
    with connection.cursor() as cursor:
        for id_articulo, cantidad in carrito.items():
            cursor.execute('SELECT precio FROM Costos WHERE id_articulo=%s ORDER BY id_precio DESC LIMIT 1', (id_articulo,))
            costo = cursor.fetchone()
            precio = costo['precio'] if costo else 0
            total = cantidad * precio
            cursor.execute('UPDATE Articulo SET stock = stock - %s WHERE id_articulo=%s', (cantidad, id_articulo))
            cursor.execute('INSERT INTO Compras (articulos_comprados, total, id_usuario, id_articulo) VALUES (%s, %s, %s, %s)', (cantidad, total, id_usuario, id_articulo))
        connection.commit()
    close_db_connection(connection)
    session['carrito'] = {}
    return redirect('/historial')

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

@app.template_filter('b64encode')
def b64encode_filter(data):
    if data:
        return base64.b64encode(data).decode('utf-8')
    return ''

@app.route('/eliminar_carrito', methods=['POST'])
def eliminar_carrito():
    from flask import request, session, jsonify
    data = request.get_json()
    id_articulo = str(data.get('id_articulo'))
    carrito = session.get('carrito', {})
    if id_articulo in carrito:
        del carrito[id_articulo]
        session['carrito'] = carrito
        session.modified = True
        return jsonify({'success': True})
    return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True)