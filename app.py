from flask import Flask, jsonify, render_template, request
from flask_httpauth import HTTPBasicAuth
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "login": "pass"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/employees', methods=['GET'])
@auth.login_required
def get_employees():
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
