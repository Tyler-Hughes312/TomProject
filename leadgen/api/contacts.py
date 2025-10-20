"""
Contacts API endpoints
"""

from flask import Blueprint, jsonify, request
from leadgen import db
from leadgen.model import Contact, Business

api = Blueprint('contacts', __name__)

@api.route('/')
def get_contacts_list():
    """Get list of contacts"""
    try:
        contacts = Contact.query.all()
        return jsonify([{
            'contactid': c.contactid,
            'business_id': c.business_id,
            'name': c.name,
            'email': c.email,
            'phone': c.phone,
            'position': c.position,
            'notes': c.notes,
            'created': c.created.isoformat() if c.created else None
        } for c in contacts])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/', methods=['POST'])
def create_contact():
    """Create a new contact"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        business_id = data.get('business_id')
        if not business_id:
            return jsonify({'error': 'business_id is required'}), 400
        
        # Check if business exists
        business = Business.query.get(business_id)
        if not business:
            return jsonify({'error': 'Business not found'}), 404
        
        contact = Contact(
            business_id=business_id,
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            position=data.get('position'),
            notes=data.get('notes')
        )
        
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({
            'contactid': contact.contactid,
            'business_id': contact.business_id,
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone,
            'position': contact.position,
            'notes': contact.notes,
            'url': f'/api/v1/contacts/{contact.contactid}/'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api.route('/<int:contact_id>/')
def get_contact_detail(contact_id):
    """Get specific contact details"""
    try:
        contact = Contact.query.get(contact_id)
        if not contact:
            return jsonify({'error': 'Contact not found'}), 404
        
        return jsonify({
            'contactid': contact.contactid,
            'business_id': contact.business_id,
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone,
            'position': contact.position,
            'notes': contact.notes,
            'created': contact.created.isoformat() if contact.created else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/<int:contact_id>/', methods=['PUT'])
def update_contact(contact_id):
    """Update a contact"""
    try:
        contact = Contact.query.get(contact_id)
        if not contact:
            return jsonify({'error': 'Contact not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        # Update fields
        if 'name' in data:
            contact.name = data['name']
        if 'email' in data:
            contact.email = data['email']
        if 'phone' in data:
            contact.phone = data['phone']
        if 'position' in data:
            contact.position = data['position']
        if 'notes' in data:
            contact.notes = data['notes']
        
        db.session.commit()
        
        return jsonify({'message': 'Contact updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api.route('/<int:contact_id>/', methods=['DELETE'])
def delete_contact(contact_id):
    """Delete a contact"""
    try:
        contact = Contact.query.get(contact_id)
        if not contact:
            return jsonify({'error': 'Contact not found'}), 404
        
        db.session.delete(contact)
        db.session.commit()
        
        return jsonify({'message': 'Contact deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
