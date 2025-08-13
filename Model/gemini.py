import google.generativeai as genai

api_key = ""
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_gemini_response(mensaje):
    """
    Recibe un mensaje de usuario y devuelve la respuesta generada por Gemini.
    """
    contexto = (
        "Esta página es un sistema de inventario web desarrollado en Flask. "
        "Permite a los usuarios ver, comprar y calificar artículos, gestionar un carrito, ver historial de compras, y a los administradores gestionar productos y usuarios. "
        "Incluye autenticación, seguridad, integración con MySQL y un asistente virtual IA para ayudar a los usuarios. "
        "Responde como asistente experto sobre el funcionamiento y características de la página si el usuario pregunta sobre ella. "
        "Si la pregunta es sobre otra cosa, responde normalmente."
    )
    prompt = f"{contexto}\nUsuario: {mensaje}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Ocurrió un error al contactar con Gemini: {str(e)}"