import sqlite3
import os

def initialize_database():
    db_path = os.path.abspath('employees.db')
    
    # Check if the database file already exists
    if os.path.exists(db_path):
        print("Database already exists. Initialization skipped.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        displayName TEXT NOT NULL,
        jobTitle TEXT NOT NULL,
        workPhoneExtension TEXT,
        department TEXT NOT NULL DEFAULT 'Unknown',
        supervisor TEXT
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    initialize_database()
