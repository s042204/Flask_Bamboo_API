from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Sample data: Employee directory
employees = [
    {"id": 1, "name": "John Doe", "position": "Software Engineer"},
    {"id": 2, "name": "Jane Smith", "position": "Product Manager"},
    {"id": 3, "name": "Emily Davis", "position": "Designer"}
]

# Users and passwords dictionary
users = {
    "admin": "secret"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/bamboo', methods=['GET'])
@auth.login_required
def get_employees():
    return jsonify(employees)

if __name__ == '__main__':
    app.run(debug=True)
