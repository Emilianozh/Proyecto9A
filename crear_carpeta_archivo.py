import os
import json

def crear_carpeta_y_archivo(data):
    # Extraer nombre de carpeta y contenido
    nombre_carpeta = data["Emi"][0]["Fecha de ingreso"]
    contenido = json.dumps(data, ensure_ascii=False, indent=4)
    # Crear carpeta si no existe
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)
    # Crear archivo txt dentro de la carpeta
    ruta_archivo = os.path.join(nombre_carpeta, "data.txt")
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)
    return ruta_archivo

# Ejemplo de uso:
data = {
    "Emi": [{
        "Fecha de ingreso": "2025",
        "Descripcion": "HAIFHHF"
    }]
}

if __name__ == "__main__":
    archivo = crear_carpeta_y_archivo(data)
    print(f"Archivo creado en: {archivo}")
