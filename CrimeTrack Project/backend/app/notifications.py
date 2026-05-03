from flask import Blueprint, request, jsonify
from app.supabase_client import supabase, supabase_admin

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/<user_id>', methods=['GET'])
def get_user_notifications(user_id):
    from app.supabase_client import verify_token
    user = verify_token(request.headers.get('Authorization'))
    if not user or str(user.id) != user_id:
        return jsonify({"error": "Forbidden"}), 403

    try:
        response = supabase_admin.table('notifications') \
            .select('*') \
            .eq('user_id', user_id) \
            .order('created_at', desc=True) \
            .limit(10) \
            .execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@notifications_bp.route('/<notification_id>/read', methods=['PUT'])
def mark_read(notification_id):
    from app.supabase_client import verify_token
    user = verify_token(request.headers.get('Authorization'))
    if not user: return jsonify({"error": "Unauthorized"}), 401

    try:
        # Verify ownership
        check = supabase_admin.table('notifications').select('user_id').eq('id', notification_id).single().execute()
        if not check.data or str(check.data['user_id']) != user.id:
            return jsonify({"error": "Forbidden"}), 403

        supabase_admin.table('notifications') \
            .update({'is_read': True}) \
            .eq('id', notification_id) \
            .execute()
        return jsonify({"message": "Notification marked as read"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
