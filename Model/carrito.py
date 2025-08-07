from flask import session, jsonify

def agregar_carrito_func(data):
    id_articulo = str(data.get('id_articulo'))
    cantidad = int(data.get('cantidad', 1))
    carrito = session.get('carrito', {})
    if id_articulo in carrito:
        carrito[id_articulo] += cantidad
    else:
        carrito[id_articulo] = cantidad
    session['carrito'] = carrito
    session.modified = True
    return jsonify({'success': True})
