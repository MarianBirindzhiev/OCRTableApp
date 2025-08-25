from utilities import generate_unique_filename, LOGGER_NAME
from PIL import Image, ImageGrab
import platform
import logging
import sys
import io

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
        pb = NSPasteboard.generalPasteboard()
        data = pb.dataForType_(NSPasteboardTypePNG) # PNG

        if data is None:
            data = pb.dataForType_(NSPasteboardTypeTIFF) # TIFF

        if data:
            try:
                img_bytes = data.bytes()
                img = Image.open(io.BytesIO(img_bytes))
                img = img.convert("RGBA")
            except Exception as e:
                logger.error(f"Failed to open image from clipboard data: {e}")
                return None

            file_path = generate_unique_filename()
            img.save(file_path, "PNG")
            logger.info(f"Saved clipboard image to: {file_path}")
            return file_path
        else:
            logger.warning("No image found in clipboard")
            return None
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