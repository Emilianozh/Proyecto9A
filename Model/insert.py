from flask import request, session, render_template, redirect, url_for
from Model.db import get_db_connection

def insert_data():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        descripcion = request.form['descripcion']
        imagen_file = request.files['imagen']
        imagen = imagen_file.read()  # Lee la imagen como binario
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO Articulo (nombre_articulo, stock, imagen, descripcion) VALUES (%s,%s,%s,%s)',(nombre, stock, imagen, descripcion))
            cursor.execute('SELECT id_articulo FROM Articulo')
            value = cursor.fetchone() 
            x = value["id_articulo"]
            x = int(x)
            print("x = ",x)
            cursor.execute('INSERT INTO Costos (precio,id_articulo) VALUES (%s,%s)',(precio,x))
            cursor.execute('SELECT id_precio FROM Costos ORDER by id_precio DESC LIMIT 1')
            value1 = cursor.fetchone() 
            y = value1["id_precio"]
            y = int(y)
            print("x = ",y)
            cursor.execute ("""UPDATE Articulo SET id_precio = %s WHERE id_articulo=%s""", (y, x))
            connection.commit()  # Commit changes to the database
        connection.close()

    return redirect(url_for('admin_view'))
