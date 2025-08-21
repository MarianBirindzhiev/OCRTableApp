from datetime import datetime
import tempfile
import os
import subprocess
from PIL import ImageGrab

def generate_screenshot_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"snip_{timestamp}.png"
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    return file_path

def get_virtual_screen_bbox():
    """
    Get virtual screen bounding box using multiple fallback methods
    for macOS Sequoia compatibility.
    """
    # Method 1: Try PIL ImageGrab to get screen dimensions
    screen = ImageGrab.grab()
    width, height = screen.size
    return 0, 0, width, height