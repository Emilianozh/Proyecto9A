from flask import request, redirect, url_for, flash
from Model.db import get_db_connection

def comprar_articulo_func(id_articulo):
    cantidad = int(request.form['cantidad'])
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT stock FROM Articulo WHERE id_articulo=%s', (id_articulo,))
        articulo = cursor.fetchone()
        if not articulo or articulo['stock'] < cantidad:
            flash('No hay suficiente stock disponible.', 'danger')
            connection.close()
            return redirect(url_for('detalle_articulo', id_articulo=id_articulo))
        # Resta la cantidad al stock
        cursor.execute('UPDATE Articulo SET stock = stock - %s WHERE id_articulo=%s', (cantidad, id_articulo))
        connection.commit()
    connection.close()
    flash('¡Compra realizada con éxito!', 'success')
    return redirect(url_for('detalle_articulo', id_articulo=id_articulo))
