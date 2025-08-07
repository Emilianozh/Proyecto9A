from flask import request, jsonify
from Model.gemini import get_gemini_response

def gemini_chat_func():
    user_msg = request.json.get('message')
    ia_text = get_gemini_response(user_msg)
    return jsonify({'response': ia_text})
