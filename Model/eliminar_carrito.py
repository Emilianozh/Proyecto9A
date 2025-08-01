from flask import request, session, jsonify

def eliminar_carrito_func():
    data = request.get_json()
    id_articulo = str(data.get('id_articulo'))
    carrito = session.get('carrito', {})
    if id_articulo in carrito:
        del carrito[id_articulo]
        session['carrito'] = carrito
        session.modified = True
        return jsonify({'success': True})
    return jsonify({'success': False})
