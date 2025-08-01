from flask import session, redirect
from Model.db import get_db_connection, close_db_connection

def finalizar_compra_func():
    id_usuario = session.get('id_usuario')
    carrito = session.get('carrito', {})
    if not carrito or not id_usuario:
        return redirect('/carrito')
    connection = get_db_connection()
    with connection.cursor() as cursor:
        for id_articulo, cantidad in carrito.items():
            cursor.execute('SELECT precio FROM Costos WHERE id_articulo=%s ORDER BY id_precio DESC LIMIT 1', (id_articulo,))
            costo = cursor.fetchone()
            precio = costo['precio'] if costo else 0
            total = cantidad * precio
            cursor.execute('UPDATE Articulo SET stock = stock - %s WHERE id_articulo=%s', (cantidad, id_articulo))
            cursor.execute('INSERT INTO Compras (articulos_comprados, total, id_usuario, id_articulo) VALUES (%s, %s, %s, %s)', (cantidad, total, id_usuario, id_articulo))
        connection.commit()
    close_db_connection(connection)
    session['carrito'] = {}
    return redirect('/historial')
