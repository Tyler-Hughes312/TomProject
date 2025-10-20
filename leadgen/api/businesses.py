"""
Businesses API endpoints
"""

from flask import Blueprint, jsonify, request
from leadgen import db
from leadgen.model import Business
from database_manager import DatabaseManager

api = Blueprint('businesses', __name__)
db_manager = DatabaseManager()

@api.route('/')
def get_businesses_list():
    """Get list of businesses with pagination"""
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    location = request.args.get('location', '')
    business_type = request.args.get('business_type', '')
    
    try:
        businesses = db_manager.get_businesses(
            page=page, 
            size=size, 
            location=location, 
            business_type=business_type
        )
        
        return jsonify({
            'results': businesses['results'],
            'total': businesses['total'],
            'page': businesses['page'],
            'size': businesses['size'],
            'total_pages': businesses['total_pages'],
            'next_page': businesses['next_page'],
            'url': request.url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/<int:business_id>/')
def get_business_detail(business_id):
    """Get specific business details"""
    try:
        business = db_manager.get_business(business_id)
        if not business:
            return jsonify({'error': 'Business not found'}), 404
        
        return jsonify(business)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/search/')
def search_businesses():
    """Search businesses by location and type"""
    location = request.args.get('location', '')
    business_type = request.args.get('business_type', '')
    radius = request.args.get('radius', 25, type=int)
    max_results = request.args.get('max_results', 100, type=int)
    
    if not location:
        return jsonify({'error': 'Location is required'}), 400
    
    try:
        from yelp_api_client import YelpAPIClient
        api_client = YelpAPIClient()
        
        businesses = api_client.search_businesses(
            location=location,
            business_type=business_type,
            radius=radius * 1609,  # Convert to meters
            max_results=max_results
        )
        
        return jsonify({
            'results': businesses,
            'total': len(businesses),
            'location': location,
            'business_type': business_type,
            'radius': radius,
            'max_results': max_results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
