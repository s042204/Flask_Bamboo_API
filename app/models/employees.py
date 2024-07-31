from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    displayName = db.Column(db.String(50), nullable=False)
    jobTitle = db.Column(db.String(50), nullable=False)
    workPhoneExtension = db.Column(db.String(20), nullable=True)
    department = db.Column(db.String(50), nullable=False, default="Unknown")
    supervisor = db.Column(db.String(50), nullable=True)
