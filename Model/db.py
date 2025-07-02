import pymysql

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='Inventario',
        cursorclass=pymysql.cursors.DictCursor  # To get results as dictionaries
    )
    return connection
def close_db_connection(connection):
    if connection:
        connection.close()