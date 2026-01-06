"""
Setup script to create the database and default admin user.
Run this once: python3 database_setup.py 
"""

import sqlite3
import configparser
from werkzeug.security import generate_password_hash

# read config
config = configparser.ConfigParser()
config.read('config.ini')
db_name = config['DATABASE']['db_name']

# Create database
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE NOT NULL,
               password_hash TEXT NOT NULL,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
               )
            ''')

# Create audit_logs table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS audit_logs (
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               username TEXT NOT NULL,
               action TEXT NOT NULL,
               timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               ip_address TEXT
               )
            ''')

# Create default admin user (password: admin123)
password_hash = generate_password_hash('admin123')
try:
    cursor.execute(
        'INSERT INTO users (username, password_hash) VALUES (?, ?)',
        ('admin', password_hash)
    )
    print("✅ Created admin user (username: admin, password: admin123)")
except sqlite3.IntegrityError:
    print("✅ Admin user already exists")

conn.commit()
conn.close()

print(f"✅ Database '{db_name}' ready!")


