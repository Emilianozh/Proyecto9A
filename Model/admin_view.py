from flask import render_template
from Model.db import get_db_connection

def admin_view_func():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT a.id_articulo, a.nombre_articulo, a.stock, c.precio
            FROM Articulo a
            LEFT JOIN Costos c ON a.id_articulo = c.id_articulo
        ''')
        articulos = cursor.fetchall()
    connection.close()
    return render_template('Module/AdminView/View/admin_view.html', articulos=articulos)
