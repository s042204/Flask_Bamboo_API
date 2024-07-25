from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_httpauth import HTTPBasicAuth
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
auth = HTTPBasicAuth()

users = {
    "login": "pass"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['logged_in'] = True
            return redirect(url_for('get_employees'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')
        

@app.route('/employees', methods=['GET'])
def get_employees():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    url = os.environ.get('BAMBOOHR_API_URL')
    token = os.environ.get('BAMBOOHR_API_TOKEN')

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {token}'
    }
    response = requests.get(url, headers=headers)
    employees = response.json().get('employees', [])
    return render_template('employees.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
