from flask import request, session, render_template, redirect, url_for
from Model.db import get_db_connection
from Model.utils import crear_directorio_usuario

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
        if value[x]["contraseña"] == password and value[x]["correo"] == mail:
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
        if usuario_data:
            crear_directorio_usuario(usuario_data)
        if admin == True:
            return redirect(url_for('admin_view'))
        else:
            return redirect(url_for('user_view'))
    else:
        error = 'Correo o contraseña incorrectos.'
        return render_template('Module/Login/View/login.html', error=error)
