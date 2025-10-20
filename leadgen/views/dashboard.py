"""
Dashboard views for Lead Generator
"""

from flask import Blueprint, render_template, jsonify, request, session, redirect
from leadgen import db
from leadgen.models import User, Business, SavedList, CustomList, ListContact
from business_finder import BusinessFinder, BusinessSearchParams
from category_helper import CategoryHelper
from leadgen.views.auth import require_auth
import os
import json
from datetime import datetime

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    """Redirect to login if not authenticated, otherwise dashboard"""
    if 'user_id' not in session:
        return redirect('/login')
    return redirect('/dashboard')

@dashboard.route('/dashboard')
@require_auth
def main_dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@dashboard.route('/list-generator')
@require_auth
def list_generator():
    """List generator page"""
    return render_template('list_generator.html')

@dashboard.route('/saved-lists')
@require_auth
def saved_lists():
    """Saved lists page"""
    return render_template('saved_lists.html')

@dashboard.route('/custom-lists')
@require_auth
def custom_lists():
    """Custom lists page"""
    return render_template('custom_lists.html')

@dashboard.route('/profile')
@require_auth
def profile():
    """User profile page"""
    return render_template('profile.html')

# API Routes

@dashboard.route('/api/v1/businesses/')
def get_businesses():
    """Get businesses from database"""
    try:
        businesses = Business.query.limit(50).all()
        return jsonify({
            'results': [business.to_dict() for business in businesses],
            'total': len(businesses)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/v1/businesses/search/')
def search_businesses():
    """Search for businesses using Yelp API with pagination"""
    try:
        # Get search parameters
        location = request.args.get('location', '')
        business_type = request.args.get('business_type', '')
        radius = float(request.args.get('radius', 25))
        max_results = int(request.args.get('max_results', 50))
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 20))
        
        if not location:
            return jsonify({'error': 'Location is required'}), 400
        
        # Check for API keys
        yelp_api_key = os.getenv('YELP_API_KEY')
        google_api_key = os.getenv('GOOGLE_API_KEY')
        
        if not yelp_api_key or not google_api_key:
            return jsonify({
                'error': 'API keys not configured',
                'message': 'Please set YELP_API_KEY and GOOGLE_API_KEY in your environment'
            }), 500
        
        # Create business finder
        finder = BusinessFinder(yelp_api_key=yelp_api_key, google_api_key=google_api_key)
        
        # Create search parameters
        params = BusinessSearchParams(
            city=location,
            industry=business_type,
            distance_miles=radius,
            max_results=max_results
        )
        
        # Search for businesses
        businesses = finder.search_yelp_businesses(params)
        
        # Convert to API format and save to database
        results = []
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        
        for business in businesses[start_idx:end_idx]:
            # Check if business already exists
            existing_business = Business.query.filter_by(yelp_id=business.get('id')).first()
            
            if not existing_business:
                # Verify address if Smarty Streets is available
                if 'address_verified' not in business:
                    business = finder.verify_business_address(business)
                
                # Create new business record
                new_business = Business(
                    yelp_id=business.get('id'),
                    name=business.get('name'),
                    address=business.get('location', {}).get('address1', ''),
                    city=business.get('location', {}).get('city', ''),
                    state=business.get('location', {}).get('state', ''),
                    zip_code=business.get('location', {}).get('zip_code', ''),
                    phone=business.get('phone', ''),
                    website=business.get('url', ''),
                    business_type=business_type,
                    rating=business.get('rating', 0),
                    review_count=business.get('review_count', 0),
                    price_level=business.get('price', ''),
                    yelp_url=business.get('url', ''),
                    # Smarty Streets verification fields
                    address_verified=business.get('address_verified', False),
                    address_verification_status=business.get('address_verification_status', 'pending'),
                    verified_address=business.get('verified_address'),
                    verified_city=business.get('verified_city'),
                    verified_state=business.get('verified_state'),
                    verified_zip_code=business.get('verified_zip_code'),
                    verification_confidence=business.get('verification_confidence', 0.0)
                )
                db.session.add(new_business)
                db.session.commit()
                existing_business = new_business
            
            results.append(existing_business.to_dict())
        
        # Check if there are more results
        has_more = end_idx < len(businesses)
        
        return jsonify({
            'results': results,
            'total': len(businesses),
            'page': page,
            'size': size,
            'has_more': has_more,
            'location': location,
            'business_type': business_type,
            'radius': radius,
            'max_results': max_results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/v1/saved-lists/')
def get_saved_lists():
    """Get user's saved lists"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        saved_lists = SavedList.query.filter_by(user_id=user_id).all()
        return jsonify({
            'results': [saved_list.to_dict() for saved_list in saved_lists],
            'total': len(saved_lists)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/v1/saved-lists/', methods=['POST'])
def create_saved_list():
    """Create a new saved list"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        search_params = data.get('search_params', '{}')
        
        if not name:
            return jsonify({'error': 'List name is required'}), 400
        
        saved_list = SavedList(
            user_id=user_id,
            name=name,
            description=description,
            search_params=search_params
        )
        
        db.session.add(saved_list)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'saved_list': saved_list.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/v1/custom-lists/')
def get_custom_lists():
    """Get user's custom lists"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        custom_lists = CustomList.query.filter_by(user_id=user_id).all()
        return jsonify({
            'results': [custom_list.to_dict() for custom_list in custom_lists],
            'total': len(custom_lists)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/v1/custom-lists/', methods=['POST'])
def create_custom_list():
    """Create a new custom list"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({'error': 'List name is required'}), 400
        
        custom_list = CustomList(
            user_id=user_id,
            name=name,
            description=description
        )
        
        db.session.add(custom_list)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'custom_list': custom_list.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/v1/contacts/save/', methods=['POST'])
def save_contact():
    """Save a contact to a list"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        business_id = data.get('business_id')
        list_type = data.get('list_type')  # 'saved' or 'custom'
        list_id = data.get('list_id')
        notes = data.get('notes', '')
        
        if not business_id or not list_type or not list_id:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if contact already exists in this list
        existing_contact = ListContact.query.filter_by(
            user_id=user_id,
            business_id=business_id,
            **{f'{list_type}_list_id': list_id}
        ).first()
        
        if existing_contact:
            return jsonify({'error': 'Contact already exists in this list'}), 400
        
        # Create new list contact
        list_contact = ListContact(
            user_id=user_id,
            business_id=business_id,
            notes=notes
        )
        
        if list_type == 'saved':
            list_contact.saved_list_id = list_id
        else:
            list_contact.custom_list_id = list_id
        
        db.session.add(list_contact)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'contact': list_contact.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/v1/categories/')
def get_categories():
    """Get available business categories"""
    try:
        helper = CategoryHelper()
        popular = helper.get_popular_categories()
        
        categories = []
        for cat in popular:
            categories.append({
                'alias': cat['alias'],
                'title': cat['title']
            })
        
        return jsonify({
            'results': categories,
            'total': len(categories)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/v1/saved-lists/<int:list_id>/', methods=['DELETE'])
def delete_saved_list(list_id):
    """Delete a saved list"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        saved_list = SavedList.query.filter_by(id=list_id, user_id=user_id).first()
        if not saved_list:
            return jsonify({'error': 'List not found'}), 404
        
        db.session.delete(saved_list)
        db.session.commit()
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/v1/custom-lists/<int:list_id>/', methods=['DELETE'])
def delete_custom_list(list_id):
    """Delete a custom list"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        custom_list = CustomList.query.filter_by(id=list_id, user_id=user_id).first()
        if not custom_list:
            return jsonify({'error': 'List not found'}), 404
        
        db.session.delete(custom_list)
        db.session.commit()
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/v1/custom-lists/<int:list_id>/businesses/')
def get_custom_list_businesses(list_id):
    """Get businesses in a custom list"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        custom_list = CustomList.query.filter_by(id=list_id, user_id=user_id).first()
        if not custom_list:
            return jsonify({'error': 'List not found'}), 404
        
        # Get list contacts for this custom list
        list_contacts = ListContact.query.filter_by(
            custom_list_id=list_id,
            user_id=user_id
        ).all()
        
        businesses = []
        for contact in list_contacts:
            business = Business.query.get(contact.business_id)
            if business:
                business_dict = business.to_dict()
                business_dict['notes'] = contact.notes
                business_dict['status'] = contact.status
                business_dict['created_at'] = contact.created_at.isoformat()
                businesses.append(business_dict)
        
        return jsonify({
            'results': businesses,
            'total': len(businesses)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/v1/profile/change-password/', methods=['POST'])
def change_password():
    """Change user password"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Current password and new password required'}), 400
        
        user = User.query.get(user_id)
        if not user.check_password(current_password):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/v1/profile/export-data/', methods=['POST'])
def export_user_data():
    """Export all user data"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Get all user data
        user = User.query.get(user_id)
        saved_lists = SavedList.query.filter_by(user_id=user_id).all()
        custom_lists = CustomList.query.filter_by(user_id=user_id).all()
        list_contacts = ListContact.query.filter_by(user_id=user_id).all()
        
        # Prepare export data
        export_data = {
            'user': user.to_dict(),
            'saved_lists': [list.to_dict() for list in saved_lists],
            'custom_lists': [list.to_dict() for list in custom_lists],
            'contacts': [contact.to_dict() for contact in list_contacts],
            'export_date': datetime.utcnow().isoformat()
        }
        
        # Create JSON response
        from flask import Response
        response = Response(
            json.dumps(export_data, indent=2),
            mimetype='application/json',
            headers={
                'Content-Disposition': f'attachment; filename=lead_generator_data_{datetime.utcnow().strftime("%Y%m%d")}.json'
            }
        )
        
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/v1/profile/delete-account/', methods=['DELETE'])
def delete_user_account():
    """Delete user account and all associated data"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Delete all user data (cascade should handle this)
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            session.clear()
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500