import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.abspath("employees.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
