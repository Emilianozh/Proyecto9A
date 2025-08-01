from flask import request, session, render_template, redirect, url_for, flash
from datetime import datetime, timedelta
from Model.db import get_db_connection

def insert_data():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        descripcion = request.form['descripcion']
        tipo_articulo = request.form['tipo_articulo']  # Nuevo campo
        imagen_file = request.files['imagen']
        imagen = imagen_file.read()  # Lee la imagen como binario
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO Articulo (nombre_articulo, stock, imagen, descripcion, tipo_articulo, fecha_creacion) VALUES (%s,%s,%s,%s,%s,NOW())',(nombre, stock, imagen, descripcion, tipo_articulo))
            cursor.execute('SELECT id_articulo FROM Articulo ORDER BY id_articulo DESC LIMIT 1')
            value = cursor.fetchone() 
            x = value["id_articulo"]
            x = int(x)
            # Guardar la fecha de inserción en sesión para mostrar el badge "Nuevo"
            if 'nuevos_articulos' not in session:
                session['nuevos_articulos'] = {}
            session['nuevos_articulos'][str(x)] = datetime.now().isoformat()
            cursor.execute('INSERT INTO Costos (precio,id_articulo) VALUES (%s,%s)',(precio,x))
            cursor.execute('SELECT id_precio FROM Costos ORDER by id_precio DESC LIMIT 1')
            value1 = cursor.fetchone() 
            y = value1["id_precio"]
            y = int(y)
            cursor.execute ("""UPDATE Articulo SET id_precio = %s WHERE id_articulo=%s""", (y, x))
            connection.commit()  # Commit changes to the database
        connection.close()

    return redirect(url_for('admin_view'))
