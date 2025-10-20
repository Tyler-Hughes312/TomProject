"""
Database models for Lead Generator
"""

from leadgen import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    saved_lists = db.relationship('SavedList', backref='user', lazy=True, cascade='all, delete-orphan')
    custom_lists = db.relationship('CustomList', backref='user', lazy=True, cascade='all, delete-orphan')
    list_contacts = db.relationship('ListContact', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Business(db.Model):
    """Business model for storing business data"""
    __tablename__ = 'businesses'
    
    id = db.Column(db.Integer, primary_key=True)
    yelp_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    phone = db.Column(db.String(50))
    website = db.Column(db.String(300))
    business_type = db.Column(db.String(100))
    rating = db.Column(db.Float)
    review_count = db.Column(db.Integer)
    price_level = db.Column(db.String(10))
    yelp_url = db.Column(db.String(300))
    # Smarty Streets verification fields
    address_verified = db.Column(db.Boolean, default=False)
    address_verification_status = db.Column(db.String(50))  # 'verified', 'invalid', 'pending'
    verified_address = db.Column(db.String(300))
    verified_city = db.Column(db.String(100))
    verified_state = db.Column(db.String(50))
    verified_zip_code = db.Column(db.String(20))
    verification_confidence = db.Column(db.Float)  # 0.0 to 1.0
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    list_contacts = db.relationship('ListContact', backref='business', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'yelp_id': self.yelp_id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'phone': self.phone,
            'website': self.website,
            'business_type': self.business_type,
            'rating': self.rating,
            'review_count': self.review_count,
            'price_level': self.price_level,
            'yelp_url': self.yelp_url,
            # Smarty Streets verification data
            'address_verified': self.address_verified,
            'address_verification_status': self.address_verification_status,
            'verified_address': self.verified_address,
            'verified_city': self.verified_city,
            'verified_state': self.verified_state,
            'verified_zip_code': self.verified_zip_code,
            'verification_confidence': self.verification_confidence,
            'created_at': self.created_at.isoformat()
        }

class SavedList(db.Model):
    """Saved list model for user's saved searches"""
    __tablename__ = 'saved_lists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    search_params = db.Column(db.Text)  # JSON string of search parameters
    business_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    list_contacts = db.relationship('ListContact', backref='saved_list', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'search_params': self.search_params,
            'business_count': self.business_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class CustomList(db.Model):
    """Custom list model for user-created lists"""
    __tablename__ = 'custom_lists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    business_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    list_contacts = db.relationship('ListContact', backref='custom_list', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'business_count': self.business_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ListContact(db.Model):
    """List contact model for linking businesses to lists"""
    __tablename__ = 'list_contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    saved_list_id = db.Column(db.Integer, db.ForeignKey('saved_lists.id'), nullable=True)
    custom_list_id = db.Column(db.Integer, db.ForeignKey('custom_lists.id'), nullable=True)
    notes = db.Column(db.Text)
    status = db.Column(db.String(50), default='new')  # new, contacted, qualified, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'business_id': self.business_id,
            'saved_list_id': self.saved_list_id,
            'custom_list_id': self.custom_list_id,
            'notes': self.notes,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
