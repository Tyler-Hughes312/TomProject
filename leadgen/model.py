"""
Database models for Lead Generator
"""

from leadgen import db
from datetime import datetime

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    filename = db.Column(db.String(120))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    leads = db.relationship('Lead', backref='user', lazy=True)
    exports = db.relationship('Export', backref='user', lazy=True)

class Business(db.Model):
    """Business model"""
    __tablename__ = 'businesses'
    
    businessid = db.Column(db.Integer, primary_key=True)
    yelp_id = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    website = db.Column(db.String(200))
    business_type = db.Column(db.String(100))
    rating = db.Column(db.Float)
    review_count = db.Column(db.Integer)
    price_level = db.Column(db.String(10))
    yelp_url = db.Column(db.String(200))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    leads = db.relationship('Lead', backref='business', lazy=True)
    contacts = db.relationship('Contact', backref='business', lazy=True)

class Lead(db.Model):
    """Lead model"""
    __tablename__ = 'leads'
    
    leadid = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.businessid'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    status = db.Column(db.String(50), default='new')
    notes = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    """Contact model"""
    __tablename__ = 'contacts'
    
    contactid = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.businessid'), nullable=False)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    position = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)

class Export(db.Model):
    """Export model"""
    __tablename__ = 'exports'
    
    exportid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    filepath = db.Column(db.String(300), nullable=False)
    record_count = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.utcnow)
