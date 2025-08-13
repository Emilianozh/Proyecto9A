from flask import request, render_template, redirect, url_for, flash
from Model.db import get_db_connection
from Model.utils import crear_directorio_usuario
import hashlib
import re

def registro_func():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        correo = request.form['correo'].strip()
        password = request.form['password']
        direccion = request.form.get('direccion', '').strip()
        telefono = request.form.get('telefono', '').strip()
        nombre_usuario = request.form.get('nombre_usuario', correo).strip()
        # Validaciones básicas
        if not nombre or not apellido or not correo or not password:
            flash('Todos los campos obligatorios deben estar completos.', 'danger')
            return redirect(url_for('registro'))
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
            return redirect(url_for('registro'))
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            flash('Correo electrónico no válido.', 'danger')
            return redirect(url_for('registro'))
        if telefono and not re.match(r'^\+?\d{7,15}$', telefono):
            flash('Teléfono no válido.', 'danger')
            return redirect(url_for('registro'))
    # Hash de la contraseña
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM Usuarios WHERE correo = %s', (correo,))
            if cursor.fetchone():
                connection.close()
                flash('El correo ya está registrado.', 'danger')
                return redirect(url_for('registro'))
            cursor.execute('''INSERT INTO Usuarios (tipo_usuario, nombre, apellido, nombre_usuario, direccion, teléfono, correo, contraseña, articulos_comprados) \
                VALUES (0, %s, %s, %s, %s, %s, %s, %s, 0)''',
                (nombre, apellido, nombre_usuario, direccion, telefono, correo, password_hash))
            connection.commit()
            # Obtener el id_usuario recién insertado
            cursor.execute('SELECT id_usuario FROM Usuarios WHERE correo = %s', (correo,))
            user_row = cursor.fetchone()
        connection.close()
        # Crear carpeta con info del usuario (contraseña en texto plano)
        if user_row:
            usuario = {
                'id_usuario': user_row['id_usuario'],
                'correo': correo,
                'password': password  # Guardar en texto plano
            }
            from Model.utils_extra import crear_directorio_usuario_func
            crear_directorio_usuario_func(usuario)
        flash('Usuario registrado exitosamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('index'))
    return render_template('Module/Login/View/registro.html')
