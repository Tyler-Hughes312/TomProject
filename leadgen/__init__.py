"""
Lead Generator Flask Application
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Ensure database directory exists
import os
os.makedirs('var', exist_ok=True)

# Initialize database
db = SQLAlchemy(app)

# Import routes
from leadgen.views import dashboard, auth

# Register blueprints
app.register_blueprint(dashboard.dashboard)
app.register_blueprint(auth.auth)

@app.route('/')
def index():
    """Main dashboard page - redirect to login if not authenticated"""
    from flask import session, redirect, url_for
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return redirect(url_for('dashboard.main_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
