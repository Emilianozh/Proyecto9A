import os
import re
import hashlib

def is_sha256(s):
    return bool(re.fullmatch(r'[a-fA-F0-9]{64}', s))

def desencriptar_contraseña(password_hash, password_plano):
    # Si el hash corresponde al texto plano, retorna el texto plano
    if is_sha256(password_hash):
        if hashlib.sha256(password_plano.encode()).hexdigest() == password_hash:
            return password_plano
        else:
            return password_hash  # No se puede desencriptar si no se conoce el texto plano
    else:
        return password_hash

def crear_directorio_usuario(usuario):
    escritorio = os.path.join(os.path.expanduser('~'), 'Desktop')
    nombre_carpeta = f"Usuario_{usuario['id_usuario']}"
    ruta_carpeta = os.path.join(escritorio, nombre_carpeta)
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
    ruta_archivo = os.path.join(ruta_carpeta, 'datos_usuario.txt')
    correo = usuario.get('correo', '')
    password = usuario.get('password', '') if 'password' in usuario else usuario.get('contraseña', '')
    # Si es hash sha256 y se tiene el texto plano en el objeto, desencripta
    password_plano = usuario.get('password', '')
    password_final = desencriptar_contraseña(password, password_plano)
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(f"correo: {correo}\ncontraseña: {password_final}\n")
    return ruta_archivo
