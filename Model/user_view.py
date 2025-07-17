from flask import render_template, request
from Model.db import get_db_connection

def user_view_func():
    tipo_articulo = request.args.get('tipo_articulo')
    connection = get_db_connection()
    with connection.cursor() as cursor:
        if tipo_articulo:
            cursor.execute('''SELECT a.id_articulo, a.nombre_articulo, a.stock, a.imagen, a.descripcion, a.tipo_articulo, c.precio
                              FROM Articulo a
                              LEFT JOIN Costos c ON a.id_articulo = c.id_articulo
                              WHERE a.tipo_articulo = %s''', (tipo_articulo,))
        else:
            cursor.execute('''SELECT a.id_articulo, a.nombre_articulo, a.stock, a.imagen, a.descripcion, a.tipo_articulo, c.precio
                              FROM Articulo a
                              LEFT JOIN Costos c ON a.id_articulo = c.id_articulo''')
        articulos = cursor.fetchall()
    connection.close()
    return render_template('Module/UserView/View/user_view.html', articulos=articulos)
