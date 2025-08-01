from flask import render_template
from Model.db import get_db_connection, close_db_connection

def admin_users_view_func():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_usuario, nombre, apellido, correo, tipo_usuario FROM Usuarios')
        usuarios = cursor.fetchall()
    close_db_connection(connection)
    return render_template('Module/AdminView/View/admin_users.html', usuarios=usuarios)
