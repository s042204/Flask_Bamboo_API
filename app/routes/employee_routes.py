from flask import Blueprint, render_template, request, redirect, url_for, session
import requests
import os
import pandas as pd
from app.models.employees import Employees
from app.db import db

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/employees', methods=['GET'])
def get_employees():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    url = os.getenv('BAMBOOHR_API_URL')
    token = os.getenv('BAMBOHR_API_TOKEN')

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {token}'
    }
    response = requests.get(url, headers=headers)
    api_employees = response.json().get('employees', [])

    for api_employee in api_employees:
        if not Employees.query.filter_by(id=api_employee['id']).first():
            new_employee = Employees(
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