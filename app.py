"""
Secure Credential & Audit Logger - Simple Flask App
Core Features: 
    - Secure login with password hashing
    - Session-based authentication
    - Audit logging of all actions
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import configparser
from functools import wraps

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
app.config['SECRET_KEY'] = config['SECURITY']['secret_key']
db_name = config['DATABASE']['db_name']


def get_db():
    """Getting database connection"""
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn


def log_event(username, action, ip_address=None):
    """Log an audit event."""
    conn = get_db()
    conn.execute(
        'INSERT INTO audit_logs (username, action, ip_address) VALUES (?, ?, ?)',
        (username, action, ip_address)
    )
    conn.commit()
    conn.close()


def login_required(f):
    """Decorator to protect routes that require login."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('login.html')

        conn = get_db()
        user = conn.execute(
            'SELECT * FROM users where username = ?',
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['username'] = username
            log_event(username, 'login_success', request.remote_addr)
            return redirect(url_for('dashboard'))
        else:
            log_event(username, 'login_failed', request.remote_addr)
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    if 'username' in session:
        log_event(session['username'], 'logout', request.remote_addr)
        session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long bro.', 'error')
            return render_template('register.html')
        
        # Checking if username already exists
        conn = get_db()
        existing = conn.execute(
            'SELECT * FROM users where username = ?',
            (username,)
        ).fetchone()

        if existing:
            conn.close()
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('register.html')
        
        # Create new user
        password_hash = generate_password_hash(password)
        conn.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        conn.commit()
        conn.close()

        log_event(username, 'user_registered', request.remote_addr)
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    logs = conn.execute("SELECT username, action, datetime(timestamp, 'localtime') as timestamp, ip_address FROM audit_logs ORDER BY timestamp DESC LIMIT 50").fetchall()
    conn.close()

    log_event(session['username'], 'view_dashboard', request.remote_addr)

    return render_template('dashboard.html', logs=logs, username=session['username'])

if __name__ == '__main__':
    port = int(config['SERVER']['port'])
    print(f"Starting Secure Audit Logger on http://127.0.0.1:{port}")
    print("Login: admin / admin123\n")
    app.run(debug=True, port=port, host='127.0.0.1')
