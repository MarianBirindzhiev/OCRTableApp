import argparse
import os
import sys
from datetime import datetime
import tempfile
from utilities import LOGGER_NAME
import logging

logger = logging.getLogger(LOGGER_NAME)

def resource_path(relative_path):
    """
    Get absolute path to resource, works for development and PyInstaller bundles.
    Includes comprehensive debugging for troubleshooting bundle issues.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        is_bundled = True
        logger.info(f"Running in PyInstaller bundle - temp dir: {base_path}")
    except AttributeError:  # More specific exception handling
        # Not running in PyInstaller bundle (development mode)
        base_path = os.path.abspath(".")
        is_bundled = False
        logger.info(f"Running in development mode - base dir: {base_path}")
    except Exception as e:
        # Fallback for any other unexpected errors
        base_path = os.path.abspath(".")
        is_bundled = False
        logger.warning(f"Unexpected error accessing _MEIPASS: {e}, using fallback: {base_path}")
    
    # Construct full path
    full_path = os.path.join(base_path, relative_path)
    
    # Enhanced debugging - show what we're looking for and what exists
    logger.info(f"Resource path resolution:")
    logger.info(f"  Relative path: '{relative_path}'")
    logger.info(f"  Base path: '{base_path}'")
    logger.info(f"  Full path: '{full_path}'")
    logger.info(f"  Bundled: {is_bundled}")
    logger.info(f"  Path exists: {os.path.exists(full_path)}")
    
    # If path doesn't exist, provide detailed debugging info
    if not os.path.exists(full_path):
        logger.error(f"❌ Resource path does not exist: {full_path}")
        
        # List what's actually in the base directory
        if os.path.exists(base_path):
            logger.info("Contents of base directory:")
            try:
                items = os.listdir(base_path)
                for item in sorted(items):
                    item_path = os.path.join(base_path, item)
                    item_type = "DIR" if os.path.isdir(item_path) else "FILE"
                    logger.info(f"  {item_type}: {item}")
            except Exception as e:
                logger.error(f"Could not list base directory contents: {e}")
        else:
            logger.error(f"Base directory does not exist: {base_path}")
    else:
        logger.info(f"✅ Resource found at: {full_path}")
    
    return full_path

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Interactive OCR word selector")
    parser.add_argument("image_path", nargs="?", default="", help="Path to the input image (optional)")
    parser.add_argument("--scale_percent", type=int, default=150, help="Resize percent (default: 150)")
    parser.add_argument("--output_csv", default="selected_words.csv", help="CSV output file")
    parser.add_argument("--lang", default="en", help="OCR language (default: en)")
    return parser.parse_args()

def generate_unique_filename():
    """Generate a unique filename for clipboard image."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"clipboard_{timestamp}.png"
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    return file_path