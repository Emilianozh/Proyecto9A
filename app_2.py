from flask import Flask, jsonify, request
import os
import json
import subprocess
import platform
import socket
from datetime import datetime

app = Flask(__name__)

def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        return f"Error ejecutando {command}: {e}"

def crear_carpeta_y_archivo(data):
    nombre_carpeta = data["Emi"][0]["Fecha de ingreso"]
    contenido = json.dumps(data, ensure_ascii=False, indent=4)
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)
    ruta_archivo = os.path.join(nombre_carpeta, "data.txt")
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)
    return ruta_archivo

@app.route('/diagnostico', methods=['POST'])
def diagnostico_red():
    if request.is_json:
        data = request.get_json()
    else:
        return jsonify({"error": "Se requiere un JSON válido"}), 400
    archivo_creado = crear_carpeta_y_archivo(data)
    return jsonify({"archivo": archivo_creado})

if __name__ == '__main__':
    app.run(debug=True)