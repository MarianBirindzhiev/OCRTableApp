from utilities import generate_unique_filename, LOGGER_NAME
from PIL import Image, ImageGrab
import platform
import logging
import sys
import io
import subprocess
import os

# macOS-only imports
if sys.platform == "darwin":
    try:
        from AppKit import NSPasteboard, NSPasteboardTypePNG, NSPasteboardTypeTIFF
    except ImportError:
        NSPasteboard = None
else:
    NSPasteboard = None


import logging

logger = logging.getLogger(LOGGER_NAME)

def get_image_from_clipboard():
    """
    Get image from clipboard (cross-platform).
    Returns the file path of the saved image, or None if no image found.
    """
    system = platform.system()
    
    if system == "darwin":  # macOS
        return _get_clipboard_image_macos()
    else:  # Windows and Linux
        return _get_clipboard_image_windows()

def _get_clipboard_image_macos():
    """Save the last image from clipboard to temp folder."""
    try:
        file_path = generate_unique_filename()
        result = subprocess.run(
            ["pngpaste", file_path], 
            check=False, 
            timeout=5
        )
        if result.returncode == 0 and os.path.exists(file_path):
            logger.info(f"Clipboard image saved via pngpaste: {file_path}")
            return file_path
        else:
            logger.warning("No image in clipboard or pngpaste failed")
            return None
    except FileNotFoundError:
        logger.error("pngpaste not installed. Install with: brew install pngpaste")
        return None
    except subprocess.TimeoutExpired:
        logger.error("pngpaste timed out while reading clipboard image")
        return None
    except Exception as e:
        logger.error(f"pngpaste error: {e}")
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