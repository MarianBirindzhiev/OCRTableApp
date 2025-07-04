from datetime import datetime
import tempfile
import os

def generate_screenshot_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"snip_{timestamp}.png"
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    return file_path