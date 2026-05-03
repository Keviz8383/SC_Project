import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from app.auth import auth_bp
from app.complaints import complaints_bp
from app.admin import admin_bp
from app.notifications import notifications_bp
from app.services import services_bp
from app.supabase_client import supabase

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for frontend integration
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(complaints_bp, url_prefix='/api/complaints')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
    app.register_blueprint(services_bp, url_prefix='/api/services')

    @app.before_request
    def check_config():
        """Ensure Supabase is configured before allowing API requests."""
        if request.endpoint and 'static' not in request.endpoint and request.endpoint != 'index':
            if supabase is None:
                logger.error("Supabase client is not initialized. Check .env configuration.")
                return jsonify({
                    "error": "Database connection not configured.",
                    "details": "Check your .env file and ensure SUPABASE_URL and SUPABASE_KEY are correct."
                }), 503

    @app.route('/')
    def index():
        return jsonify({
            "message": "Welcome to CrimeTrack API", 
            "status": "Online",
            "version": "1.0.0"
        }), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal Server Error: {error}")
        return jsonify({
            "error": "Internal server error",
            "details": str(error) if Config.DEBUG else "Please check server logs."
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"Unhandled Exception: {e}")
        return jsonify({
            "error": "Unexpected Service Error",
            "details": str(e) if Config.DEBUG else "An unexpected error occurred."
        }), 500

    @app.route('/favicon.ico')
    def favicon():
        return '', 204

    return app

if __name__ == '__main__':
    # Validate config before running
    if not Config.validate():
        logger.critical("Failed to validate configuration. Exiting.")
        exit(1)
        
    app = create_app()
    logger.info(f"Starting CrimeTrack Backend in {'DEBUG' if Config.DEBUG else 'PROD'} mode...")
    app.run(debug=Config.DEBUG, port=5000, host='0.0.0.0')
