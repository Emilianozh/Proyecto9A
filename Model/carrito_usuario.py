from flask import render_template, session
from Model.db import get_db_connection, close_db_connection

def carrito_usuario_func():
    carrito = session.get('carrito', {})
    articulos = []
    total = 0
    if carrito:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            for id_articulo, cantidad in carrito.items():
                cursor.execute('''SELECT a.id_articulo, a.nombre_articulo, a.imagen, c.precio FROM Articulo a LEFT JOIN Costos c ON a.id_articulo = c.id_articulo WHERE a.id_articulo = %s''', (id_articulo,))
                articulo = cursor.fetchone()
                if articulo:
                    articulo['cantidad'] = cantidad
                    articulo['subtotal'] = cantidad * articulo['precio']
                    total += articulo['subtotal']
                    articulos.append(articulo)
        close_db_connection(connection)
    return render_template('Module/UserView/View/carrito.html', articulos=articulos, total=total)
