from flask import Blueprint, request, jsonify
from services.gemini_service import process_prescription_image, process_prescription_text
from utils.validators import validate_image_file, get_mime_type
import logging
import asyncio

logger = logging.getLogger(__name__)

medication_bp = Blueprint('medication', __name__)


@medication_bp.route('/process-medication-image', methods=['POST'])
def process_medication_image_endpoint():
    """
    Process a prescription image and extract medication data
    
    Expected: multipart/form-data with 'image' file
    Returns: JSON with extracted medication data
    """
    try:
        logger.info("📸 Received prescription image processing request")
        
        # Check if file is present
        if 'image' not in request.files:
            logger.warning("❌ No image file in request")
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files['image']
        
        # Validate file
        is_valid, error_message = validate_image_file(file)
        if not is_valid:
            logger.warning(f"❌ Invalid file: {error_message}")
            return jsonify({
                'success': False,
                'error': error_message
            }), 400
        
        # Read file data
        image_data = file.read()
        mime_type = get_mime_type(file.filename)
        
        logger.info(f"📁 Processing {file.filename} ({mime_type}, {len(image_data)} bytes)")
        
        # Process with Gemini (run async function)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            process_prescription_image(image_data, mime_type)
        )
        loop.close()
        
        logger.info("Successfully processed prescription image")
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
    except Exception as e:
        logger.error(f"❌ Processing error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to process prescription image. Please try again.'
        }), 500


@medication_bp.route('/process-medication-text', methods=['POST'])
def process_medication_text_endpoint():
    """
    Process a natural language prescription description and extract medication data.

    Expected JSON body:
    {
        "text": "I take 500mg Metformin every morning after breakfast"
    }

    Returns:
        JSON with extracted medication data (same format as image endpoint)
    """
    try:
        logger.info("📝 Received prescription text processing request")

        if not request.is_json:
            logger.warning("❌ Request content type is not JSON")
            return jsonify({
                'success': False,
                'error': 'Request must be JSON with a "text" field'
            }), 400

        data = request.get_json(silent=True) or {}
        text = data.get('text', '')

        if not text or not text.strip():
            logger.warning("❌ No text provided in request")
            return jsonify({
                'success': False,
                'error': 'Text is required'
            }), 400

        # Process with Gemini (text)
        result = process_prescription_text(text)

        logger.info("✅ Successfully processed prescription text")

        return jsonify({
            'success': True,
            'data': result
        }), 200

    except ValueError as e:
        logger.error(f"Validation error (text): {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

    except Exception as e:
        logger.error(f"❌ Text processing error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to process prescription text. Please try again.'
        }), 500
