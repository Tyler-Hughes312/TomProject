"""
Leads API endpoints
"""

from flask import Blueprint, jsonify, request
from leadgen import db
from leadgen.model import Lead, Business, User
from database_manager import DatabaseManager

api = Blueprint('leads', __name__)
db_manager = DatabaseManager()

@api.route('/')
def get_leads_list():
    """Get list of leads with pagination"""
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    
    try:
        leads = db_manager.get_leads(page=page, size=size)
        
        return jsonify({
            'results': leads['results'],
            'total': leads['total'],
            'page': leads['page'],
            'size': leads['size'],
            'total_pages': leads['total_pages'],
            'next_page': leads['next_page'],
            'url': request.url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/', methods=['POST'])
def create_new_lead():
    """Create a new lead"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        business_id = data.get('business_id')
        user_id = data.get('user_id', 1)  # Default to user 1
        notes = data.get('notes', '')
        
        if not business_id:
            return jsonify({'error': 'business_id is required'}), 400
        
        # Check if business exists
        business = db_manager.get_business(business_id)
        if not business:
            return jsonify({'error': 'Business not found'}), 404
        
        # Create lead
        lead_id = db_manager.create_lead(business_id, user_id, notes)
        
        return jsonify({
            'leadid': lead_id,
            'business_id': business_id,
            'user_id': user_id,
            'notes': notes,
            'url': f'/api/v1/leads/{lead_id}/'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/<int:lead_id>/')
def get_lead_detail(lead_id):
    """Get specific lead details"""
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT l.leadid, l.business_id, l.user_id, l.status, l.notes, l.created,
                       b.name, b.address, b.phone, b.website
                FROM leads l
                JOIN businesses b ON l.business_id = b.businessid
                WHERE l.leadid = ?
            """, (lead_id,))
            
            row = cursor.fetchone()
            if not row:
                return jsonify({'error': 'Lead not found'}), 404
            
            return jsonify({
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/<int:lead_id>/', methods=['PUT'])
def update_lead(lead_id):
    """Update a lead"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if lead exists
            cursor.execute("SELECT leadid FROM leads WHERE leadid = ?", (lead_id,))
            if not cursor.fetchone():
                return jsonify({'error': 'Lead not found'}), 404
            
            # Update lead
            updates = []
            params = []
            
            if 'status' in data:
                updates.append("status = ?")
                params.append(data['status'])
            
            if 'notes' in data:
                updates.append("notes = ?")
                params.append(data['notes'])
            
            if updates:
                params.append(lead_id)
                cursor.execute(f"""
                    UPDATE leads 
                    SET {', '.join(updates)}
                    WHERE leadid = ?
                """, params)
                conn.commit()
            
            return jsonify({'message': 'Lead updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/<int:lead_id>/', methods=['DELETE'])
def delete_lead(lead_id):
    """Delete a lead"""
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if lead exists
            cursor.execute("SELECT leadid FROM leads WHERE leadid = ?", (lead_id,))
            if not cursor.fetchone():
                return jsonify({'error': 'Lead not found'}), 404
            
            # Delete lead
            cursor.execute("DELETE FROM leads WHERE leadid = ?", (lead_id,))
            conn.commit()
            
            return jsonify({'message': 'Lead deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
