from flask import request, redirect, url_for
from Model.db import get_db_connection

def eliminar_articulo():
    if request.method == 'POST':
        id_articulo = request.form.get('id_articulo')
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Eliminar primero las compras relacionadas
            cursor.execute('DELETE FROM Compras WHERE id_articulo = %s', (id_articulo,))
            # Eliminar de Costos si existe relación
            cursor.execute('DELETE FROM Costos WHERE id_articulo = %s', (id_articulo,))
            # Luego eliminar de Articulo
            cursor.execute('DELETE FROM Articulo WHERE id_articulo = %s', (id_articulo,))
            connection.commit()
        connection.close()
        return redirect(url_for('admin_view'))
    return redirect(url_for('admin_view'))
