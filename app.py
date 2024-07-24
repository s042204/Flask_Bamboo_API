from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# Sample data: Employee directory
employees = [
    {"id": 1, "name": "John Doe", "position": "Software Engineer"},
    {"id": 2, "name": "Jane Smith", "position": "Product Manager"},
    {"id": 3, "name": "Emily Davis", "position": "Designer"}
]

# In-memory user store for simplicity
users = {
    "test": generate_password_hash("pass")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/bamboo', methods=['GET'])
@auth.login_required
def get_employees():
    return jsonify(employees)

if __name__ == '__main__':
    app.run(debug=True)
