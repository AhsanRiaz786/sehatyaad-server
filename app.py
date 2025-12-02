from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.medication import medication_bp
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": Config.ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Register blueprints
app.register_blueprint(medication_bp, url_prefix='/api')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SehatYaad Backend',
        'version': '1.0.0'
    }), 200


@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'SehatYaad Backend API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'process_image': '/api/process-medication-image (POST)'
        }
    }), 200


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB.'
    }), 413


@app.errorhandler(500)
def internal_server_error(error):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    logger.info("🚀 Starting SehatYaad Backend Server...")
    logger.info(f"📍 Server running on http://0.0.0.0:{Config.PORT}")
    logger.info(f"🔧 Environment: {Config.FLASK_ENV}")
    logger.info(f"🌐 CORS enabled for: {Config.ALLOWED_ORIGINS}")
    
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )
