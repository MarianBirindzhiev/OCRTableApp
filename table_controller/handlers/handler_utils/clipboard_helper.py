from utilities import generate_unique_filename, LOGGER_NAME
from PIL import ImageGrab
import logging

logger = logging.getLogger(LOGGER_NAME)

def get_image_from_clipboard():
    """
    Get image from clipboard (cross-platform).
    Returns the file path of the saved image, or None if no image found.
    """
    try:
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

