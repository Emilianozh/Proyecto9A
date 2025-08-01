from flask import request, redirect, url_for, flash, session
from Model.db import get_db_connection

def comprar_articulo_func(id_articulo):
    cantidad = int(request.form['cantidad'])
    id_usuario = session.get('id_usuario')
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT stock FROM Articulo WHERE id_articulo=%s', (id_articulo,))
        articulo = cursor.fetchone()
        if not articulo or articulo['stock'] < cantidad:
            flash('No hay suficiente stock disponible.', 'danger')
            connection.close()
            return redirect(url_for('detalle_articulo', id_articulo=id_articulo))
        # Obtener precio actual
        cursor.execute('SELECT precio FROM Costos WHERE id_articulo=%s ORDER BY id_precio DESC LIMIT 1', (id_articulo,))
        costo = cursor.fetchone()
        precio = costo['precio'] if costo else 0
        total = cantidad * precio
        # Resta la cantidad al stock
        cursor.execute('UPDATE Articulo SET stock = stock - %s WHERE id_articulo=%s', (cantidad, id_articulo))
        # Registrar la compra en la tabla Compras, ahora con id_articulo
        cursor.execute('INSERT INTO Compras (articulos_comprados, total, id_usuario, id_articulo) VALUES (%s, %s, %s, %s)', (cantidad, total, id_usuario, id_articulo))
        connection.commit()
    connection.close()
    flash('¡Compra realizada con éxito!', 'success')
    return redirect(url_for('detalle_articulo', id_articulo=id_articulo))
