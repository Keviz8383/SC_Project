from supabase import create_client, Client
from config import Config
import logging

logger = logging.getLogger(__name__)

# Initialize Supabase client lazily or safely
supabase: Client = None
supabase_admin: Client = None

if Config.validate():
    try:
        supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        supabase_admin = create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_ROLE_KEY)
        logger.info("Supabase clients initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Supabase: {e}")

def verify_token(auth_header):
    """Verify JWT token and return user or None."""
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(" ")[1]
    try:
        # We use the anon client reach out to Supabase Auth to verify the token
        # Note: get_user() automatically validates the token with Supabase Auth
        res = supabase.auth.get_user(token)
        if res and hasattr(res, 'user'):
            return res.user
        return None
    except Exception as e:
        logger.debug(f"Token verification failed: {e}")
        return None
