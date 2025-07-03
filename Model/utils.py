import os
import json

def crear_directorio_usuario(usuario):
    escritorio = os.path.join(os.path.expanduser('~'), 'Desktop')
    nombre_carpeta = f"Usuario_{usuario['id_usuario']}"
    ruta_carpeta = os.path.join(escritorio, nombre_carpeta)
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
    ruta_archivo = os.path.join(ruta_carpeta, 'datos_usuario.txt')
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(json.dumps(usuario, ensure_ascii=False, indent=4))
    return ruta_archivo
