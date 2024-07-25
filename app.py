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

# Dummy data
local_employees = []

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
    api_employees = response.json().get('employees', [])

    for employee in api_employees:
        employee['local'] = False

    for employee in local_employees:
        employee['local'] = True

    combined_employees = api_employees + local_employees

    return render_template('employees.html', employees=combined_employees)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    name = request.form['name']
    position = request.form['position']
    extension = request.form['extension']
    department = request.form['department']
    supervisor = request.form['supervisor']
    new_employee = {
        "id": len(local_employees) + 1,
        "displayName": name,
        "jobTitle": position,
        "workPhoneExtension": extension,
        "department": department,
        "supervisor": supervisor,
        "local": True
    }
    local_employees.append(new_employee)
    return redirect(url_for('get_employees'))

@app.route('/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    global local_employees
    local_employees = [emp for emp in local_employees if emp["id"] != employee_id]
    return redirect(url_for('get_employees'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
