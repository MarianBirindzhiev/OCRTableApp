from datetime import datetime
import tempfile
import os
import subprocess
import mss
from PIL import ImageGrab
import platform

def generate_screenshot_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"snip_{timestamp}.png"
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    return file_path

def get_virtual_screen_bbox():
    """
    Get the bounding box of the virtual screen across monitors.
    Uses mss (cross-platform).
    """
    system = platform.system()
    if system == "Darwin":
        img = ImageGrab.grab()
        width, height = img.size
        return 0, 0, width, height
    else:
        with mss.mss() as sct:
            monitor = sct.monitors[0]  # virtual bounding box for all displays
            return monitor["left"], monitor["top"], monitor["width"], monitor["height"]
    
def capture_region(x1, y1, x2, y2, save_path):
    """
    Cross-platform region capture.
    - On Windows: mss
    - On macOS: use native screencapture CLI
    """
    system = platform.system()

    if system == "Darwin":  # macOS
        # Use screencapture CLI
        width = x2 - x1
        height = y2 - y1
        region = f"{x1},{y1},{width},{height}"
        subprocess.run(
            ["screencapture", "-x", "-R", region, save_path],
            check=True
        )
        return save_path
    
    else:
        with mss.mss() as sct:
            monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=save_path)
