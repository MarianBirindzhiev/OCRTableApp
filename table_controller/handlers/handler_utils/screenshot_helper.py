from datetime import datetime
import tempfile
import os
import subprocess
import mss
from PIL import ImageGrab, Image
import platform


def get_virtual_screen_bbox():
    """
    Get the bounding box of the virtual screen across monitors.
    """
    with mss.mss() as sct:
        monitor = sct.monitors[0]  # virtual bounding box for all displays
        return monitor["left"], monitor["top"], monitor["width"], monitor["height"]
    