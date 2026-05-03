from flask import Blueprint, request, jsonify
from app.supabase_client import supabase, supabase_admin
import uuid

complaints_bp = Blueprint('complaints', __name__)

@complaints_bp.route('/', methods=['POST'])
def create_complaint():
    from app.supabase_client import verify_token
    user = verify_token(request.headers.get('Authorization'))
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    title = data.get('title')
    description = data.get('description')
    category = data.get('category')
    
    if not all([title, description, category]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        complaint_id = str(uuid.uuid4())[:8].upper()
        insert_data = {
            'id': complaint_id,
            'user_id': user.id,
            'title': title,
            'description': description,
            'category': category,
            'location_lat': data.get('location_lat'),
            'location_lng': data.get('location_lng'),
            'location_address': data.get('location_address'),
            'status': 'Submitted'
        }
        
        supabase_admin.table('complaints').insert(insert_data).execute()
        supabase_admin.table('status_updates').insert({
            'complaint_id': complaint_id,
            'status': 'Submitted',
            'remarks': 'Complaint received by the system.',
            'updated_by': user.id
        }).execute()
        
        return jsonify({"message": "Success", "complaint_id": complaint_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@complaints_bp.route('/user/<user_id>', methods=['GET'])
def get_user_complaints(user_id):
    from app.supabase_client import verify_token
    user = verify_token(request.headers.get('Authorization'))
    if not user or str(user.id) != user_id:
        return jsonify({"error": "Forbidden"}), 403

    try:
        response = supabase_admin.table('complaints').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@complaints_bp.route('/<complaint_id>', methods=['GET'])
def get_complaint_details(complaint_id):
    try:
        # Use admin client to bypass RLS for case tracking by ID
        complaint = supabase_admin.table('complaints').select('*').eq('id', complaint_id).single().execute()
        
        # Get status updates/history
        status_history = supabase_admin.table('status_updates').select('*').eq('complaint_id', complaint_id).order('updated_at', desc=True).execute()
        
        # Get evidence
        evidence = supabase_admin.table('evidence').select('*').eq('complaint_id', complaint_id).execute()
        
        return jsonify({
            "complaint": complaint.data,
            "history": status_history.data,
            "evidence": evidence.data
        }), 200
    except Exception as e:
        # Graceful handling if ID is invalid
        if 'PGRST116' in str(e):
            return jsonify({"error": "No record found with this Case ID."}), 404
        return jsonify({"error": str(e)}), 500

@complaints_bp.route('/upload-evidence', methods=['POST'])
def upload_evidence():
    from app.supabase_client import verify_token
    user = verify_token(request.headers.get('Authorization'))
    if not user: return jsonify({"error": "Unauthorized"}), 401

    complaint_id = request.form.get('complaint_id')
    file = request.files.get('file')
    
    if not complaint_id or not file:
        return jsonify({"error": "Missing data"}), 400
        
    try:
        # Verify ownership before upload
        check = supabase_admin.table('complaints').select('user_id').eq('id', complaint_id).single().execute()
        if not check.data or str(check.data['user_id']) != user.id:
            return jsonify({"error": "Unauthorized access"}), 403

        file_path = f"evidence/{complaint_id}/{file.filename}"
        supabase_admin.storage.from_('crime-evidence').upload(file_path, file.read())
        file_url = supabase_admin.storage.from_('crime-evidence').get_public_url(file_path)
        
        supabase_admin.table('evidence').insert({
            'complaint_id': complaint_id,
            'file_url': file_url,
            'file_name': file.filename
        }).execute()
        
        return jsonify({"message": "Success", "url": file_url}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
