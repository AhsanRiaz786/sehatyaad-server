from werkzeug.datastructures import FileStorage
from config import Config
import imghdr


def validate_image_file(file: FileStorage) -> tuple[bool, str]:
    """
    Validate uploaded image file
    
    Args:
        file: Uploaded file from request
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not file:
        return False, "No file provided"
    
    if file.filename == '':
        return False, "No file selected"
    
    # Check file extension
    if '.' in file.filename:
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext not in Config.ALLOWED_EXTENSIONS:
            return False, f"Invalid file type. Allowed: {', '.join(Config.ALLOWED_EXTENSIONS)}"
    else:
        return False, "File has no extension"
    
    # Verify it's actually an image
    file.seek(0)
    header = file.read(512)
    file.seek(0)
    
    format_type = imghdr.what(None, header)
    if format_type not in ['png', 'jpeg', 'gif']:
        return False, "File is not a valid image"
    
    return True, ""


def get_mime_type(filename: str) -> str:
    """Get MIME type from filename"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    mime_types = {
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',
        'heic': 'image/heic'
    }
    
    return mime_types.get(ext, 'image/jpeg')
