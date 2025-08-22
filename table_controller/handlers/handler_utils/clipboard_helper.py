from utilities import generate_unique_filename

from PIL import Image, ImageGrab
import tempfile
import os
import platform
import subprocess
from datetime import datetime
from utilities import LOGGER_NAME
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
    """Get image from clipboard on macOS using pngpaste or osascript."""
    try:
        # Method 1: Try using pngpaste (if installed)
        file_path = generate_unique_filename()
        result = subprocess.run(
            ["pngpaste", file_path], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0 and os.path.exists(file_path):
            logger.info(f"Clipboard image saved via pngpaste: {file_path}")
            return file_path
    except FileNotFoundError:
        logger.debug("pngpaste not found, trying osascript method")
    
    try:
        # Method 2: Use osascript
        file_path = generate_unique_filename()
        script = f'''
        set the clipboard to (the clipboard as «class PNGf»)
        set png_data to (the clipboard as «class PNGf»)
        set file_path to "{file_path}"
        set file_ref to open for access file_path with write permission
        write png_data to file_ref
        close access file_ref
        '''
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and os.path.exists(file_path):
            logger.info(f"Clipboard image saved via osascript: {file_path}")
            return file_path
    except Exception as e:
        logger.error(f"Failed to get clipboard image on macOS: {e}")
    
    return None

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