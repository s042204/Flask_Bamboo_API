from flask import Flask, render_template, request, redirect, url_for, session
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
import requests
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
auth = HTTPBasicAuth()

# Setup database
db_path = os.path.abspath('employees.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User authentication
users = {
    "login": "pass"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

# Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    displayName = db.Column(db.String(50), nullable=False)
    jobTitle = db.Column(db.String(50), nullable=False)
    workPhoneExtension = db.Column(db.String(20), nullable=True)
    department = db.Column(db.String(50), nullable=False, default="Unknown")
    supervisor = db.Column(db.String(50), nullable=True)

# Routes
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

    for api_employee in api_employees:
        if not Employee.query.filter_by(id=api_employee['id']).first():
            new_employee = Employee(
                id=api_employee['id'],
                displayName=api_employee.get('displayName', 'N/A'),
                jobTitle=api_employee.get('jobTitle', 'N/A'),
                workPhoneExtension=api_employee.get('workPhoneExtension', ''),
                department=api_employee.get('department', 'Unknown'),
                supervisor=api_employee.get('supervisor', '')
            )
            db.session.add(new_employee)
    db.session.commit()

    df = pd.DataFrame(api_employees)

    return render_template('employees.html', employees=api_employees, table=df.to_html(classes='data', header="true"))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
