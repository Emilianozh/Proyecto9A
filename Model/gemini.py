import google.generativeai as genai

api_key = ""
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_gemini_response(mensaje):
    """
    Recibe un mensaje de usuario y devuelve la respuesta generada por Gemini.
    """
    try:
        response = model.generate_content(mensaje)
        return response.text.strip()
    except Exception as e:
        return f"Ocurrió un error al contactar con Gemini: {str(e)}"