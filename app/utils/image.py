from io import BytesIO
from PIL import Image
import logging

logger = logging.getLogger(__name__)

# Register HEIC/HEIF support
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    logger.info("HEIC/HEIF support registered")
except ImportError:
    logger.warning("pillow-heif not available, HEIC support disabled")

# Supported image formats
SUPPORTED_FORMATS = {
    'JPEG': ['jpg', 'jpeg', 'jpe'],
    'PNG': ['png'],
    'WEBP': ['webp'],
    'HEIC': ['heic', 'heif'],
    'GIF': ['gif'],
    'BMP': ['bmp', 'dib'],
    'TIFF': ['tiff', 'tif'],
    'ICO': ['ico'],
    'PPM': ['ppm'],
}

def get_image_format(image_bytes):
    """Detect image format from bytes"""
    try:
        img = Image.open(BytesIO(image_bytes))
        return img.format
    except Exception as e:
        logger.warning(f"Could not detect format: {e}")
        return None

def load_image(image_bytes):
    """Load image from bytes and convert to RGB"""
    if not image_bytes:
        raise ValueError("Image bytes cannot be empty")
    
    try:
        img = Image.open(BytesIO(image_bytes))
        logger.info(f"Loaded image format: {img.format}, mode: {img.mode}")
        
        # Convert RGBA to RGB (handle transparency)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create white background for transparency
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            return background
        elif img.mode != 'RGB':
            return img.convert('RGB')
        else:
            return img
    except Exception as e:
        logger.error(f"Failed to load image: {e}")
        raise ValueError(f"Could not load image: {str(e)}. Supported formats: JPEG, PNG, WEBP, HEIC, GIF, BMP, TIFF, ICO")
