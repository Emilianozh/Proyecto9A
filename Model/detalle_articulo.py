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
        # Obtener promedio y conteo de estrellas
        cursor.execute('''
            SELECT COUNT(*) as total, AVG(estrellas) as promedio
            FROM Opiniones
            WHERE id_articulo = %s
        ''', (id_articulo,))
        rating_info = cursor.fetchone() or {'total': 0, 'promedio': 0}
        # Obtener distribución de estrellas (1-5)
        cursor.execute('''
            SELECT estrellas, COUNT(*) as cantidad
            FROM Opiniones
            WHERE id_articulo = %s
            GROUP BY estrellas
        ''', (id_articulo,))
        distribucion = {i: 0 for i in range(1, 6)}
        for row in cursor.fetchall():
            distribucion[row['estrellas']] = row['cantidad']
        # Obtener comentarios con usuario (sin fecha, solo visual)
        cursor.execute('''
            SELECT o.comentario, o.estrellas, o.id_usuario, u.nombre, u.apellido
            FROM Opiniones o
            JOIN Usuarios u ON o.id_usuario = u.id_usuario
            WHERE o.id_articulo = %s AND o.comentario IS NOT NULL AND o.comentario != ''
        ''', (id_articulo,))
        comentarios = cursor.fetchall()
    connection.close()
    return render_template('Module/UserView/View/detalle_articulo.html', articulo=articulo, rating_info=rating_info, distribucion=distribucion, comentarios=comentarios)
