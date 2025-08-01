from flask import render_template, request, session
from datetime import datetime, timedelta
from Model.db import get_db_connection

def user_view_func():
    tipo_articulo = request.args.get('tipo_articulo')
    connection = get_db_connection()
    with connection.cursor() as cursor:
        if tipo_articulo:
            cursor.execute('''SELECT a.id_articulo, a.nombre_articulo, a.stock, a.imagen, a.descripcion, a.tipo_articulo, a.fecha_creacion, c.precio
                              FROM Articulo a
                              LEFT JOIN Costos c ON a.id_articulo = c.id_articulo
                              WHERE a.tipo_articulo = %s''', (tipo_articulo,))
        else:
            cursor.execute('''SELECT a.id_articulo, a.nombre_articulo, a.stock, a.imagen, a.descripcion, a.tipo_articulo, a.fecha_creacion, c.precio
                              FROM Articulo a
                              LEFT JOIN Costos c ON a.id_articulo = c.id_articulo''')
        articulos = cursor.fetchall()
    connection.close()
    ahora = datetime.now()
    nuevos = [a for a in articulos if a['fecha_creacion'] and (ahora - a['fecha_creacion']).total_seconds() < 300]
    no_nuevos = [a for a in articulos if not (a['fecha_creacion'] and (ahora - a['fecha_creacion']).total_seconds() < 300)]
    articulos_ordenados = nuevos + no_nuevos
    return render_template('Module/UserView/View/user_view.html', articulos=articulos_ordenados, ahora=ahora)
