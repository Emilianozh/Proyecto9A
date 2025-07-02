from Model import insert
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import subprocess
import platform
import socket
from datetime import datetime
from Model.login import login
from Model.insert import insert_data as insert
from Model.db import get_db_connection
from Model.admin_view import admin_view_func




app = Flask(__name__)

app.secret_key = 'supersecretkey'  # Necesario para sesiones

@app.route('/')
def index():
    return render_template('Module/Login/View/login.html')

@app.route('/admin_view', methods=['GET'])
def admin_view():
    return admin_view_func()

@app.route('/insert_view', methods=['GET'])
def insert_view():
    return render_template('Module/InsertView/View/insert_view.html')

@app.route('/login', methods=['POST'])
def login_route():
    return login()

@app.route('/insertar', methods=['POST'])
def insertar_route():
    return insert()

if __name__ == '__main__':
    app.run(debug=True)