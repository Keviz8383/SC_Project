import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    @staticmethod
    def validate():
        """Ensure all required environment variables are set and not placeholders."""
        configs = {
            "SUPABASE_URL": Config.SUPABASE_URL,
            "SUPABASE_KEY": Config.SUPABASE_KEY,
            "SUPABASE_SERVICE_ROLE_KEY": Config.SUPABASE_SERVICE_ROLE_KEY
        }
        
        placeholders = ["your-project-url", "your-anon", "your-service"]
        missing = []

        for key, val in configs.items():
            if not val or any(p in str(val).lower() for p in placeholders):
                missing.append(key)
        
        if missing:
            print(f"\n[CRITICAL ERROR] Missing or invalid API keys in .env: {', '.join(missing)}")
            print("Please update your .env file with actual keys from the Supabase Dashboard.\n")
            return False
        return True
