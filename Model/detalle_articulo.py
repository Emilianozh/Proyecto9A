from flask import render_template
from Model.db import get_db_connection

def detalle_articulo_func(id_articulo):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT a.id_articulo, a.nombre_articulo, a.imagen, a.stock, a.descripcion, c.precio
            FROM Articulo a
            LEFT JOIN Costos c ON a.id_articulo = c.id_articulo
            WHERE a.id_articulo = %s
        ''', (id_articulo,))
        articulo = cursor.fetchone()
    connection.close()
    return render_template('Module/UserView/View/detalle_articulo.html', articulo=articulo)
