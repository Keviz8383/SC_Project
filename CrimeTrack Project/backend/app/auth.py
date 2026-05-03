from flask import Blueprint, request, jsonify
from app.supabase_client import supabase, supabase_admin

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'citizen')  # default to citizen
    name = data.get('name')

    if not email or not password or not name:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Use Admin Auth Client to bypass rate limits and auto-confirm emails for the demo
        response = supabase_admin.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True
        })
        
        if not response.user:
            return jsonify({"error": "Registration failed. Verify your Supabase Service Role Key."}), 400

        # Create user profile with role in 'profiles' table
        profile_data = {
            'id': response.user.id,
            'email': email,
            'name': name,
            'role': role
        }
        supabase_admin.table('profiles').insert(profile_data).execute()
        
        return jsonify({
            "message": "User registered successfully",
            "user_id": response.user.id
        }), 201
        
    except Exception as e:
        error_msg = str(e).lower()
        print(f"Registration Error Log: {error_msg}") # For debugging
        
        # More robust matching for common Supabase errors
        if 'already registered' in error_msg or 'user_already_exists' in error_msg:
            return jsonify({"error": "This email is already registered."}), 400
        
        if 'email rate limit exceeded' in error_msg or 'over_rate_limit' in error_msg:
            return jsonify({
                "error": "Registration Limit Exceeded",
                "details": "Safety limit reached. Please wait a few minutes or use a different network."
            }), 429
            
        return jsonify({
            "error": "Backend Service Error",
            "details": str(e)
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.session:
            try:
                # Fetch user profile using admin client to bypass initial RLS restrictions
                profile_response = supabase_admin.table('profiles').select('*').eq('id', response.user.id).single().execute()
                user_data = profile_response.data
            except Exception as profile_err:
                if 'PGRST116' in str(profile_err):
                    return jsonify({
                        "error": "Profile Not Found",
                        "details": "Success! You are authenticated, but your CrimeTrack profile is missing. Please register via the Sign Up tab."
                    }), 404
                return jsonify({"error": f"Profile Fetch Error: {str(profile_err)}"}), 500
            
            return jsonify({
                "session": {
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                    "expires_in": response.session.expires_in
                },
                "user": user_data
            }), 200
            
        return jsonify({"error": "Invalid credentials"}), 401
        
    except Exception as e:
        error_msg = str(e).lower()
        if 'email not confirmed' in error_msg:
            return jsonify({
                "error": "Email Not Verified",
                "details": "Please check your inbox or disable 'Confirm Email' in Supabase Settings."
            }), 401
            
        return jsonify({"error": f"Login Error: {str(e)}"}), 500

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    from app.supabase_client import verify_token
    user = verify_token(request.headers.get('Authorization'))
    
    if not user:
        return jsonify({"error": "Unauthorized or session expired"}), 401
        
    try:
        profile_response = supabase_admin.table('profiles').select('*').eq('id', user.id).single().execute()
        return jsonify(profile_response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401
