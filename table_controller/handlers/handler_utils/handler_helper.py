from datetime import datetime
import tempfile
import os
from PIL import ImageGrab

def capture_screenshot_to_tmp():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    tmp_dir = tempfile.gettempdir()  # Use the system temp directory
    full_path = os.path.join(tmp_dir, filename)
    screenshot = ImageGrab.grab()
    screenshot = screenshot.convert("RGB")  # Ensure it's in a standard format
    screenshot.save(full_path, format="PNG")
    return str(full_path)