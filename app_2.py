from flask import Flask, jsonify
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

@app.route('/diagnostico', methods=['POST'])
def diagnostico_red():
    data ={
        "Emi": [{
            "Fecha de ingreso":"2025",
            "Descripcion": "HAIFHHF"
    }
  ]
}
    system_info = {
                "Carpeta": run_command("cd"),
                "crear_directorio": run_command("mkdir test_directory"),
                "crear_archivo": run_command("echo  > test_directory/test_file.txt"),
    }
    return jsonify(system_info)

if __name__ == '__main__':
    app.run(debug=True)