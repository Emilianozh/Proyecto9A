from flask import request, session, redirect, url_for, flash
from Model.db import get_db_connection

def editar_usuario_func():
    if 'id_usuario' not in session:
        flash('Debes iniciar sesión para editar tus datos.', 'danger')
        return redirect(url_for('index'))
    id_usuario = session['id_usuario']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    if not nombre or not apellido or not correo:
        flash('Todos los campos son obligatorios.', 'warning')
        return redirect(url_for('user_view'))
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('UPDATE Usuarios SET nombre=%s, apellido=%s, correo=%s WHERE id_usuario=%s', (nombre, apellido, correo, id_usuario))
        connection.commit()
    connection.close()
    # Actualiza la sesión
    session['nombre_usuario'] = nombre
    session['apellido_usuario'] = apellido
    session['correo'] = correo
    flash('Datos actualizados correctamente.', 'success')
    return redirect(url_for('user_view'))
