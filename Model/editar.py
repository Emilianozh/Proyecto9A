from flask import request, redirect, url_for, jsonify
from Model.db import get_db_connection

def editar_articulo():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            id_articulo = data.get('id_articulo')
            nombre = data.get('nombre')
            stock = data.get('stock')
            precio = data.get('precio')
        else:
            id_articulo = request.form.get('id_articulo')
            nombre = request.form.get('nombre')
            stock = request.form.get('stock')
            precio = request.form.get('precio')
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute('UPDATE Articulo SET nombre_articulo=%s, stock=%s WHERE id_articulo=%s', (nombre, stock, id_articulo))
            cursor.execute('UPDATE Costos SET precio=%s WHERE id_articulo=%s', (precio, id_articulo))
            connection.commit()
        connection.close()
        if request.is_json:
            return jsonify({'success': True})
        return redirect(url_for('admin_view'))
    if request.is_json:
        return jsonify({'success': False}), 400
    return redirect(url_for('admin_view'))
