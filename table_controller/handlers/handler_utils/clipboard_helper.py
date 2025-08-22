from utilities import generate_unique_filename
from utilities import LOGGER_NAME

from PIL import Image, ImageGrab
import tempfile
import os
import platform
import subprocess
from datetime import datetime


import logging

logger = logging.getLogger(LOGGER_NAME)

def get_image_from_clipboard():
    """
    Get image from clipboard (cross-platform).
    Returns the file path of the saved image, or None if no image found.
    """
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return _get_clipboard_image_macos()
    else:  # Windows and Linux
        return _get_clipboard_image_windows()

def _get_clipboard_image_macos():
    """Save the last image from clipboard to temp folder."""
    from AppKit import NSPasteboard, NSPasteboardTypePNG
    
    pb = NSPasteboard.generalPasteboard()
    data = pb.dataForType_(NSPasteboardTypePNG)

    if not data:
        print("No image found in clipboard.")
        return None

    # Convert NSData → bytes → Pillow Image
    img_bytes = data.bytes().tobytes()
    img = Image.open(io.BytesIO(img_bytes))

    file_path = generate_unique_filename()
    img.save(file_path, "PNG")
    print(f"Saved clipboard image to: {file_path}")
    return file_path

def _get_clipboard_image_windows():
    """Get image from clipboard on Windows using PIL."""
    try:
        # Use PIL ImageGrab for Windows/Linux
        img = ImageGrab.grabclipboard()
        if img is not None:
            file_path = generate_unique_filename()
            img.save(file_path, "PNG")
            logger.info(f"Clipboard image saved: {file_path}")
            return file_path
        else:
            logger.warning("No image found in clipboard")
            return None
    except Exception as e:
        logger.error(f"Failed to get clipboard image: {e}")
        return None