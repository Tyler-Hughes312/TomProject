"""
Authentication views for Lead Generator
Matching LegislationForDumbies pattern
"""

from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from leadgen import db
from leadgen.models import User
import os

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication - matching LegislationForDumbies pattern"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard.main_dashboard'))
    
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page and user creation - matching LegislationForDumbies pattern"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            return render_template('register.html')
        
        if password != confirm_password:
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth.route('/logout')
def logout():
    """Logout user - matching LegislationForDumbies pattern"""
    session.clear()
    return redirect(url_for('auth.login'))

@auth.route('/api/auth/status')
def auth_status():
    """Check authentication status - matching LegislationForDumbies pattern"""
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return jsonify({
                'authenticated': True,
                'user': user.to_dict()
            })
    
    return jsonify({'authenticated': False})

def require_auth(f):
    """Decorator to require authentication - matching LegislationForDumbies pattern"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function