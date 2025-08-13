from flask import request, session, jsonify
from Model.opinion import guardar_opinion

def calificar_articulo_func():
    data = request.get_json()
    id_usuario = session.get('id_usuario')
    id_articulo = data.get('id_articulo')
    estrellas = int(data.get('estrellas', 0))
    comentario = data.get('comentario', '').strip()
    print(f"[CALIFICAR] id_usuario={id_usuario}, id_articulo={id_articulo}, estrellas={estrellas}, comentario={comentario}")
    if not (id_usuario and id_articulo and estrellas):
        print("[CALIFICAR] Datos incompletos o inválidos")
        return jsonify({'success': False})
    try:
        guardar_opinion(id_usuario, id_articulo, estrellas, comentario if comentario else None)
        print("[CALIFICAR] Inserción exitosa")
        return jsonify({'success': True})
    except Exception as e:
        print(f"[CALIFICAR] Error al insertar: {e}")
        return jsonify({'success': False, 'error': str(e)})
