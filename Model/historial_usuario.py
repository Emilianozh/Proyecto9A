from flask import render_template, session
from Model.db import get_db_connection, close_db_connection

def historial_usuario_func():
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return render_template('Module/UserView/View/historial.html', compras=[])
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('''SELECT c.id_compra, c.total, c.articulos_comprados, a.nombre_articulo, a.imagen
                          FROM Compras c
                          JOIN Articulo a ON a.id_articulo = c.id_articulo
                          WHERE c.id_usuario = %s
                          ORDER BY c.id_compra DESC''', (id_usuario,))
        compras = cursor.fetchall()
    close_db_connection(connection)
    return render_template('Module/UserView/View/historial.html', compras=compras)
