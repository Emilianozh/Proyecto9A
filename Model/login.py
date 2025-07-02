from flask import request, session, render_template, redirect, url_for
from Model.db import get_db_connection

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
    for x in range(0,len(value)):
        if value[x]["contraseña"] == password and value[x]["correo"] == mail:
            existe = True
            sesion = True
            session['correo'] = mail
            session['id_usuario'] = value[x]["id_usuario"]
            session['nombre_usuario'] = value[x]["nombre"]
            session['apellido_usuario'] = value[x]["apellido"]
            if value[x]["tipo_usuario"]==True:
                admin = True
                session['correo'] = mail
            else:
                print("")
        else:
            print("")

    if existe == True:
        if admin == True:
            return redirect(url_for('admin_view'))
        else:
            return render_template('Module/UserView/View/user_view.html')
    else:
        return render_template('index.html')
