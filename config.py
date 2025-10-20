"""
Configuration for Lead Generator
Based on existing business finder patterns
"""

import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List, Dict, Optional

load_dotenv()

# API Configuration
YELP_API_KEY = os.getenv('YELP_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL', os.path.abspath('var/leadgen.sqlite3'))
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

@dataclass
class BusinessSearchParams:
    """Parameters for business search - matching existing pattern"""
    city: str
    industry: str
    distance_miles: float
    max_results: int = 50

# Business Categories (matching existing pattern)
BUSINESS_CATEGORIES = {
    'restaurants': 'restaurants',
    'retail': 'shopping',
    'beauty': 'beautysvc',
    'fitness': 'fitness',
    'healthcare': 'health',
    'automotive': 'auto',
    'professional': 'professional',
    'entertainment': 'arts',
    'real_estate': 'realestate',
    'legal': 'lawyers',
    'financial': 'financialservices',
    'education': 'education',
    'home_services': 'homeservices',
    'hotels': 'hotelstravel',
    'nightlife': 'nightlife',
    'pets': 'pets',
    'religious': 'religiousorgs',
    'local_services': 'localservices'
}

# Default Settings
DEFAULT_LIMIT = 50
MAX_RESULTS = 1000
LEADS_PER_PAGE = 10
UPLOAD_FOLDER = 'var/uploads'
OUTPUT_FOLDER = 'output/exports'

# Excel Export Columns
EXCEL_COLUMNS = [
    'Business Name',
    'Address',
    'City',
    'State',
    'ZIP Code',
    'Phone Number',
    'Website URL',
    'Business Type',
    'Rating',
    'Review Count',
    'Price Level',
    'Yelp URL'
]

# Flask Configuration
class Config:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_URL}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
