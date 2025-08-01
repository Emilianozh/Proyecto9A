from Model.db import get_db_connection, close_db_connection

def guardar_opinion(id_usuario, id_articulo, estrellas, comentario=None):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        if comentario:
            cursor.execute('INSERT INTO Opiniones (id_usuario, id_articulo, estrellas, comentario) VALUES (%s, %s, %s, %s)', (id_usuario, id_articulo, estrellas, comentario))
        else:
            cursor.execute('INSERT INTO Opiniones (id_usuario, id_articulo, estrellas) VALUES (%s, %s, %s)', (id_usuario, id_articulo, estrellas))
        connection.commit()
    close_db_connection(connection)
    return True
