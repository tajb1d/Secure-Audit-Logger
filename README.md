# 🔐 Secure Audit Logger

A professional-grade Flask web application designed to demonstrate secure authentication, session management, and automated audit logging. This project implements security best practices to prevent common web vulnerabilities.

## 🚀 Key Features
* **Secure Authentication**: User registration and login using hashed passwords (Werkzeug).
* **Automated Audit Logging**: Every system event (logins, registrations, failures) is recorded with timestamps and IP addresses.
* **Session Security**: Protected routes using Flask sessions to prevent unauthorized access to the dashboard.
* **Database Integration**: SQLite backend for persistent data storage.
* **Modern UI**: Fully responsive frontend styled with professional CSS and dynamic Flash messaging.

## 🛠️ Technical Stack
* **Backend**: Python / Flask
* **Frontend**: HTML5 / CSS3 / Jinja2 Templates
* **Database**: SQLite
* **Version Control**: Git / GitHub

## 📂 Project Structure
* `app.py`: The core application logic and route handlers.
* `database_setup.py`: Script to initialize the SQLite schema.
* `static/`: Contains the global `style.css` for consistent UI.
* `templates/`: Jinja2 templates for Login, Register, and Dashboard views.
* `.gitignore`: Ensures sensitive files like `audit.db` and `config.ini` remain private.

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/tajb1d/Secure-Audit-Logger.git](https://github.com/tajb1d/Secure-Audit-Logger.git)
   cd Secure-Audit-Logger

2. **Set up Virtual Environment**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt

4. **Configuration**: 

Copy config.ini.example to config.ini and add your unique secret_key.

5. Initialize Database:
    ```bash
    python database_setup.py

6. Run Application:
    ```bash
    python app.py