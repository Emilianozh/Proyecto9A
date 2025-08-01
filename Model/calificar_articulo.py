from flask import request, session, jsonify
from Model.opinion import guardar_opinion

def calificar_articulo_func():
    data = request.get_json()
    id_usuario = session.get('id_usuario')
    id_articulo = data.get('id_articulo')
    estrellas = int(data.get('estrellas', 0))
    comentario = data.get('comentario', '').strip()
    if not (id_usuario and id_articulo and estrellas):
        return jsonify({'success': False})
    guardar_opinion(id_usuario, id_articulo, estrellas, comentario if comentario else None)
    return jsonify({'success': True})
