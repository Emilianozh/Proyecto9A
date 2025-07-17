from flask import Blueprint, redirect, url_for, session, request, render_template
from oauthlib.oauth2 import WebApplicationClient
import requests
import os
import json
from Model.db import get_db_connection, close_db_connection

# Configuración (puedes poner tus credenciales aquí para pruebas locales)
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID") or "AQUI_TU_CLIENT_ID"
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET") or "AQUI_TU_CLIENT_SECRET"
GOOGLE_DISCOVERY_URL = os.environ.get("GOOGLE_DISCOVERY_URL", "https://accounts.google.com/.well-known/openid-configuration")

google_bp = Blueprint('google_bp', __name__)
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Permitir HTTP en desarrollo local
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@google_bp.route("/login/google")
def login_google():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for("google_bp.callback", _external=True),
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@google_bp.route("/login/google/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=url_for("google_bp.callback", _external=True),
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    userinfo = userinfo_response.json()
    session["user"] = userinfo

    # --- INICIO: Manejo de usuario en base de datos ---
    correo = userinfo.get("email")
    nombre = userinfo.get("given_name", "")
    apellido = userinfo.get("family_name", "")
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_usuario, tipo_usuario, correo, nombre, apellido FROM Usuarios WHERE correo=%s', (correo,))
        user_db = cursor.fetchone()
        if not user_db:
            # Insertar usuario como tipo_usuario=2 (usuario normal)
            cursor.execute('INSERT INTO Usuarios (correo, nombre, apellido, tipo_usuario) VALUES (%s, %s, %s, %s)', (correo, nombre, apellido, 2))
            connection.commit()
            cursor.execute('SELECT id_usuario, tipo_usuario, correo, nombre, apellido FROM Usuarios WHERE correo=%s', (correo,))
            user_db = cursor.fetchone()
    close_db_connection(connection)
    session['correo'] = correo
    session['id_usuario'] = user_db['id_usuario']
    session['nombre_usuario'] = user_db['nombre']
    session['apellido_usuario'] = user_db['apellido']
    session['tipo_usuario'] = user_db['tipo_usuario']
    # --- FIN: Manejo de usuario en base de datos ---

    if user_db['tipo_usuario'] == 1:
        return redirect(url_for("admin_view"))
    else:
        return redirect(url_for("user_view"))
