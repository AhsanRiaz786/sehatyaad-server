import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    # Gemini API
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = FLASK_ENV == 'development'
    
    # CORS
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')
    
    # Upload settings
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB default
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic'}
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required in .env file")
        return True


# Validate config on import
Config.validate()
