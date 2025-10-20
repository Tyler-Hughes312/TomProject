"""
Database Manager for Lead Generator
Handles SQLite database operations
"""

import sqlite3
import os
import uuid
from typing import List, Dict, Optional
from config import DATABASE_URL, UPLOAD_FOLDER

class DatabaseManager:
    def __init__(self, db_path: str = DATABASE_URL):
        self.db_path = db_path
        self.ensure_db_directory()
    
    def ensure_db_directory(self):
        """Ensure database directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    def create_tables(self):
        """Create Lead Generator database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    userid INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    fullname TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    filename TEXT,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Businesses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS businesses (
                    businessid INTEGER PRIMARY KEY AUTOINCREMENT,
                    yelp_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    address TEXT,
                    city TEXT,
                    state TEXT,
                    zip_code TEXT,
                    phone TEXT,
                    website TEXT,
                    business_type TEXT,
                    rating REAL,
                    review_count INTEGER,
                    price_level TEXT,
                    yelp_url TEXT,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Leads table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS leads (
                    leadid INTEGER PRIMARY KEY AUTOINCREMENT,
                    business_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    status TEXT DEFAULT 'new',
                    notes TEXT,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (business_id) REFERENCES businesses(businessid),
                    FOREIGN KEY (user_id) REFERENCES users(userid)
                )
            """)
            
            # Contacts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    contactid INTEGER PRIMARY KEY AUTOINCREMENT,
                    business_id INTEGER NOT NULL,
                    name TEXT,
                    email TEXT,
                    phone TEXT,
                    position TEXT,
                    notes TEXT,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (business_id) REFERENCES businesses(businessid)
                )
            """)
            
            # Exports table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS exports (
                    exportid INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    filename TEXT NOT NULL,
                    filepath TEXT NOT NULL,
                    record_count INTEGER,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(userid)
                )
            """)
            
            conn.commit()
    
    def reset_database(self):
        """Reset database with sample data"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.create_tables()
        self.add_sample_data()
    
    def add_sample_data(self):
        """Add sample data for testing"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Add sample users
            cursor.execute("""
                INSERT OR IGNORE INTO users (username, fullname, email, filename)
                VALUES ('admin', 'Administrator', 'admin@leadgen.com', 'admin.jpg')
            """)
            
            # Add sample businesses
            sample_businesses = [
                ('yelp_1', 'Sample Restaurant', '123 Main St', 'Nashville', 'TN', '37201', 
                 '615-555-0123', 'https://samplerestaurant.com', 'restaurants', 4.5, 150, '$$', 
                 'https://yelp.com/biz/sample-restaurant'),
                ('yelp_2', 'Sample Retail Store', '456 Oak Ave', 'Nashville', 'TN', '37202', 
                 '615-555-0124', 'https://sampleretail.com', 'retail', 4.2, 89, '$', 
                 'https://yelp.com/biz/sample-retail'),
                ('yelp_3', 'Sample Beauty Salon', '789 Pine St', 'Nashville', 'TN', '37203', 
                 '615-555-0125', 'https://samplebeauty.com', 'beauty', 4.8, 67, '$$$', 
                 'https://yelp.com/biz/sample-beauty')
            ]
            
            for business in sample_businesses:
                cursor.execute("""
                    INSERT OR IGNORE INTO businesses 
                    (yelp_id, name, address, city, state, zip_code, phone, website, 
                     business_type, rating, review_count, price_level, yelp_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, business)
            
            # Add sample leads
            cursor.execute("""
                INSERT OR IGNORE INTO leads (business_id, user_id, status, notes)
                VALUES (1, 1, 'new', 'Initial contact made')
            """)
            
            conn.commit()
    
    def get_businesses(self, page: int = 1, size: int = 10, location: str = '', 
                     business_type: str = '') -> Dict:
        """Get businesses with pagination"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Build WHERE clause
            where_conditions = []
            params = []
            
            if location:
                where_conditions.append("(city LIKE ? OR address LIKE ?)")
                params.extend([f'%{location}%', f'%{location}%'])
            
            if business_type:
                where_conditions.append("business_type = ?")
                params.append(business_type)
            
            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
            
            # Get total count
            cursor.execute(f"SELECT COUNT(*) FROM businesses WHERE {where_clause}", params)
            total = cursor.fetchone()[0]
            
            # Get businesses with pagination
            offset = (page - 1) * size
            cursor.execute(f"""
                SELECT businessid, yelp_id, name, address, city, state, zip_code, 
                       phone, website, business_type, rating, review_count, price_level, yelp_url
                FROM businesses 
                WHERE {where_clause}
                ORDER BY created DESC
                LIMIT ? OFFSET ?
            """, params + [size, offset])
            
            businesses = []
            for row in cursor.fetchall():
                businesses.append({
                    'businessid': row[0],
                    'yelp_id': row[1],
                    'name': row[2],
                    'address': row[3],
                    'city': row[4],
                    'state': row[5],
                    'zip_code': row[6],
                    'phone': row[7],
                    'website': row[8],
                    'business_type': row[9],
                    'rating': row[10],
                    'review_count': row[11],
                    'price_level': row[12],
                    'yelp_url': row[13]
                })
            
            # Calculate pagination info
            total_pages = (total + size - 1) // size
            next_page = page + 1 if page < total_pages else None
            
            return {
                'results': businesses,
                'total': total,
                'page': page,
                'size': size,
                'total_pages': total_pages,
                'next_page': next_page
            }
    
    def get_business(self, business_id: int) -> Optional[Dict]:
        """Get specific business by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT businessid, yelp_id, name, address, city, state, zip_code, 
                       phone, website, business_type, rating, review_count, price_level, yelp_url
                FROM businesses 
                WHERE businessid = ?
            """, (business_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return {
                'businessid': row[0],
                'yelp_id': row[1],
                'name': row[2],
                'address': row[3],
                'city': row[4],
                'state': row[5],
                'zip_code': row[6],
                'phone': row[7],
                'website': row[8],
                'business_type': row[9],
                'rating': row[10],
                'review_count': row[11],
                'price_level': row[12],
                'yelp_url': row[13]
            }
    
    def create_lead(self, business_id: int, user_id: int, notes: str = '') -> int:
        """Create a new lead"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO leads (business_id, user_id, notes)
                VALUES (?, ?, ?)
            """, (business_id, user_id, notes))
            return cursor.lastrowid
    
    def get_leads(self, page: int = 1, size: int = 10) -> Dict:
        """Get leads with pagination"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute("SELECT COUNT(*) FROM leads")
            total = cursor.fetchone()[0]
            
            # Get leads with pagination
            offset = (page - 1) * size
            cursor.execute("""
                SELECT l.leadid, l.business_id, l.user_id, l.status, l.notes, l.created,
                       b.name, b.address, b.phone, b.website
                FROM leads l
                JOIN businesses b ON l.business_id = b.businessid
                ORDER BY l.created DESC
                LIMIT ? OFFSET ?
            """, (size, offset))
            
            leads = []
            for row in cursor.fetchall():
                leads.append({
                    'leadid': row[0],
                    'business_id': row[1],
                    'user_id': row[2],
                    'status': row[3],
                    'notes': row[4],
                    'created': row[5],
                    'business_name': row[6],
                    'business_address': row[7],
                    'business_phone': row[8],
                    'business_website': row[9]
                })
            
            # Calculate pagination info
            total_pages = (total + size - 1) // size
            next_page = page + 1 if page < total_pages else None
            
            return {
                'results': leads,
                'total': total,
                'page': page,
                'size': size,
                'total_pages': total_pages,
                'next_page': next_page
            }
