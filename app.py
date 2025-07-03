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





app = Flask(__name__)

app.secret_key = 'supersecretkey'  # Necesario para sesiones

# Registro del blueprint de Google login


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

if __name__ == '__main__':
    app.run(debug=True)