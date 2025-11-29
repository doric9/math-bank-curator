"""File handling utilities"""

import os
import logging
from typing import Dict, Any
from bs4 import BeautifulSoup
from src.image_utils import is_supported_image_type

logger = logging.getLogger(__name__)

def read_file_content(file_path: str) -> Dict[str, Any]:
    """
    Read content from various file types, extracting text and images.

    Args:
        file_path: Path to file

    Returns:
        Dictionary with 'text' and 'images' (list of bytes)

    Raises:
        ValueError: If file type not supported
        RuntimeError: If reading fails
    """
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == '.txt' or ext == '.md':
            # Plain text files
            with open(file_path, 'r', encoding='utf-8') as f:
                return {"text": f.read(), "images": []}

        elif ext == '.pdf':
            # PDF files - requires PyPDF2
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    text = ""
                    images = []
                    
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                        
                        # Extract images from page
                        if hasattr(page, 'images'):
                            for img in page.images:
                                # Filter supported image types based on extension or name
                                img_name = img.name.lower()
                                mime_type = 'application/octet-stream'
                                if img_name.endswith('.jpg') or img_name.endswith('.jpeg'):
                                    mime_type = 'image/jpeg'
                                elif img_name.endswith('.png'):
                                    mime_type = 'image/png'
                                elif img_name.endswith('.webp'):
                                    mime_type = 'image/webp'
                                elif img_name.endswith('.heic'):
                                    mime_type = 'image/heic'
                                elif img_name.endswith('.heif'):
                                    mime_type = 'image/heif'
                                
                                if is_supported_image_type(mime_type):
                                    images.append({
                                        "mime_type": mime_type,
                                        "data": img.data
                                    })
                    
                    return {"text": text, "images": images}
            except ImportError:
                raise RuntimeError(
                    "PyPDF2 not installed. Install with: pip install PyPDF2"
                )

        elif ext in ['.html', '.htm']:
            # HTML files - simplistic image extraction not supported for local HTML yet
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            return {"text": text, "images": []}

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        raise RuntimeError(f"Failed to read file: {e}")
