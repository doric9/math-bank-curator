"""Image processing utilities"""

import logging
import requests
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

SUPPORTED_IMAGE_TYPES = {
    'image/jpeg', 'image/png', 'image/webp', 'image/heic', 'image/heif'
}

def is_supported_image_type(mime_type: str) -> bool:
    """Check if the image MIME type is supported"""
    return mime_type.lower() in SUPPORTED_IMAGE_TYPES

def download_image(url: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
    """
    Download an image from a URL.
    
    Args:
        url: Image URL
        timeout: Request timeout
        
    Returns:
        Dictionary with mime_type and data, or None if failed/unsupported
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        
        if response.status_code == 200:
            mime_type = response.headers.get('content-type', '').lower()
            if is_supported_image_type(mime_type):
                return {
                    "mime_type": mime_type,
                    "data": response.content
                }
            else:
                logger.warning(f"Skipping unsupported image type: {mime_type}")
    except Exception as e:
        logger.warning(f"Failed to download image {url}: {e}")
        
    return None
