from flask import Blueprint, request, jsonify
from app.supabase_client import supabase, supabase_admin

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/complaints', methods=['GET'])
def get_all_complaints():
    from app.supabase_client import verify_token
    user = verify_token(request.headers.get('Authorization'))
    if not user: return jsonify({"error": "Unauthorized"}), 401

    try:
        # Verify role in DB
        profile = supabase_admin.table('profiles').select('role').eq('id', user.id).single().execute()
        if not profile.data or profile.data['role'] != 'admin':
            return jsonify({"error": "Forbidden: Admin access required"}), 403

        response = supabase_admin.table('complaints').select('*').order('created_at', desc=True).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/update-status', methods=['POST'])
def update_complaint_status():
    from app.supabase_client import verify_token
    user = verify_token(request.headers.get('Authorization'))
    if not user: return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    complaint_id = data.get('complaint_id')
    new_status = data.get('status')
    remarks = data.get('remarks')

    try:
        # Verify admin role
        profile = supabase_admin.table('profiles').select('role').eq('id', user.id).single().execute()
        if not profile.data or profile.data['role'] != 'admin':
            return jsonify({"error": "Forbidden"}), 403

        # Update status
        supabase_admin.table('complaints').update({'status': new_status}).eq('id', complaint_id).execute()
        
        # Get owner for notification
        complaint_res = supabase_admin.table('complaints').select('user_id').eq('id', complaint_id).single().execute()
        
        # Insert audit trail
        supabase_admin.table('status_updates').insert({
            'complaint_id': complaint_id,
            'status': new_status,
            'remarks': remarks,
            'updated_by': user.id
        }).execute()

        # Create notification
        if complaint_res.data:
            supabase_admin.table('notifications').insert({
                'user_id': complaint_res.data['user_id'],
                'message': f"Update: Complaint {complaint_id} is now '{new_status}'."
            }).execute()
        
        return jsonify({"message": "Status updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/analytics', methods=['GET'])
def get_analytics():
    try:
        # Fetch data for Chart.js stats
        complaints_response = supabase.table('complaints').select('status, category').execute()
        
        # Aggregation can be done here or in the frontend
        # For simplicity, returning the raw data
        return jsonify(complaints_response.data), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
