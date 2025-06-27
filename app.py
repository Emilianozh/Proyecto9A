from flask import Flask, jsonify,  render_template
import subprocess
import platform
import socket
from datetime import datetime



app = Flask(__name__)



 
@app.route('/')
def index():
    return render_template('Module/Login/View/login.html')

@app.route('/admin_view', methods=['GET'])
def admin_view():
    return render_template('Module/AdminView/View/admin_view.html')

@app.route('/insert_view', methods=['GET'])
def insert_view():
    return render_template('Module/InsertView/View/insert_view.html')


if __name__ == '__main__':
    app.run(debug=True)