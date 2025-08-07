from flask import request, session, render_template, redirect, url_for
from Model.db import get_db_connection
import hashlib
import re

def is_sha256(s):
    return isinstance(s, str) and bool(re.fullmatch(r'[a-fA-F0-9]{64}', s))

def login():
    mail = request.form['mail']
    password = request.form['password']
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_usuario, tipo_usuario, correo, contraseña, nombre, apellido FROM Usuarios')
        value = cursor.fetchall()
        connection.close()
    sesion = False
    existe = False
    admin = False
    usuario_data = None
    for x in range(0,len(value)):
        db_pass = value[x]["contraseña"]
        # Si la contraseña guardada es un hash sha256, comparar con el hash
        if is_sha256(db_pass):
            password_check = hashlib.sha256(password.encode()).hexdigest()
        else:
            password_check = password
        if db_pass == password_check and value[x]["correo"] == mail:
            existe = True
            sesion = True
            session['correo'] = mail
            session['id_usuario'] = value[x]["id_usuario"]
            session['nombre_usuario'] = value[x]["nombre"]
            session['apellido_usuario'] = value[x]["apellido"]
            usuario_data = value[x]
            if value[x]["tipo_usuario"]==True:
                admin = True
                session['correo'] = mail
            else:
                print("")
        else:
            print("")

    if existe == True:
        # Ya no crear carpeta al iniciar sesión
        if admin == True:
            return redirect(url_for('admin_view'))
        else:
            return redirect(url_for('user_view'))
    else:
        error = 'Correo o contraseña incorrectos.'
        return render_template('Module/Login/View/login.html', error=error)
