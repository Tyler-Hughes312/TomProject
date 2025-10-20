"""
Exports API endpoints
"""

from flask import Blueprint, jsonify, request, send_file
from leadgen import db
from leadgen.model import Export, Business, Lead
from excel_generator import ExcelGenerator
import os

api = Blueprint('exports', __name__)
excel_gen = ExcelGenerator()

@api.route('/')
def get_exports_list():
    """Get list of exports"""
    try:
        exports = Export.query.all()
        return jsonify([{
            'exportid': e.exportid,
            'user_id': e.user_id,
            'filename': e.filename,
            'filepath': e.filepath,
            'record_count': e.record_count,
            'created': e.created.isoformat() if e.created else None
        } for e in exports])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/businesses/', methods=['POST'])
def export_businesses():
    """Export businesses to Excel"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        # Get businesses to export
        business_ids = data.get('business_ids', [])
        if not business_ids:
            # Export all businesses
            businesses = Business.query.all()
        else:
            businesses = Business.query.filter(Business.businessid.in_(business_ids)).all()
        
        if not businesses:
            return jsonify({'error': 'No businesses found to export'}), 404
        
        # Convert to dict format
        business_data = []
        for business in businesses:
            business_data.append({
                'name': business.name,
                'address': business.address,
                'city': business.city,
                'state': business.state,
                'zip_code': business.zip_code,
                'phone': business.phone,
                'website': business.website,
                'business_type': business.business_type,
                'rating': business.rating,
                'review_count': business.review_count,
                'price_level': business.price_level,
                'yelp_url': business.yelp_url
            })
        
        # Generate Excel file
        filename = data.get('filename', f'business_export_{len(business_data)}_records.xlsx')
        filepath = excel_gen.export_to_excel(businesses=business_data, filename=filename)
        
        # Save export record
        export = Export(
            user_id=data.get('user_id', 1),
            filename=os.path.basename(filepath),
            filepath=filepath,
            record_count=len(business_data)
        )
        db.session.add(export)
        db.session.commit()
        
        return jsonify({
            'exportid': export.exportid,
            'filename': export.filename,
            'filepath': export.filepath,
            'record_count': export.record_count,
            'url': f'/api/v1/exports/{export.exportid}/download/'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api.route('/leads/', methods=['POST'])
def export_leads():
    """Export leads to Excel"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        # Get leads to export
        lead_ids = data.get('lead_ids', [])
        if not lead_ids:
            # Export all leads
            leads = Lead.query.all()
        else:
            leads = Lead.query.filter(Lead.leadid.in_(lead_ids)).all()
        
        if not leads:
            return jsonify({'error': 'No leads found to export'}), 404
        
        # Convert to dict format
        lead_data = []
        for lead in leads:
            lead_data.append({
                'leadid': lead.leadid,
                'business_name': lead.business.name if lead.business else 'Unknown',
                'business_address': lead.business.address if lead.business else '',
                'business_phone': lead.business.phone if lead.business else '',
                'business_website': lead.business.website if lead.business else '',
                'status': lead.status,
                'notes': lead.notes,
                'created': lead.created.isoformat() if lead.created else None
            })
        
        # Generate Excel file
        filename = data.get('filename', f'leads_export_{len(lead_data)}_records.xlsx')
        filepath = excel_gen.export_leads_to_excel(leads=lead_data, filename=filename)
        
        # Save export record
        export = Export(
            user_id=data.get('user_id', 1),
            filename=os.path.basename(filepath),
            filepath=filepath,
            record_count=len(lead_data)
        )
        db.session.add(export)
        db.session.commit()
        
        return jsonify({
            'exportid': export.exportid,
            'filename': export.filename,
            'filepath': export.filepath,
            'record_count': export.record_count,
            'url': f'/api/v1/exports/{export.exportid}/download/'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api.route('/<int:export_id>/download/')
def download_export(export_id):
    """Download export file"""
    try:
        export = Export.query.get(export_id)
        if not export:
            return jsonify({'error': 'Export not found'}), 404
        
        if not os.path.exists(export.filepath):
            return jsonify({'error': 'Export file not found'}), 404
        
        return send_file(
            export.filepath,
            as_attachment=True,
            download_name=export.filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
