from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__)

users = {
    "login": "pass"
}

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['logged_in'] = True
            return redirect(url_for('employee.get_employees'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')
