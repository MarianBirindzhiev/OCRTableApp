import argparse
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Interactive OCR word selector")
    parser.add_argument("image_path", nargs="?", default="", help="Path to the input image (optional)")
    parser.add_argument("--scale_percent", type=int, default=150, help="Resize percent (default: 150)")
    parser.add_argument("--output_csv", default="selected_words.csv", help="CSV output file")
    parser.add_argument("--lang", default="en", help="OCR language (default: en)")
    return parser.parse_args()