from enum import Enum
from dataclasses import dataclass

class InteractionMode(Enum):
    """
    Enum for interaction modes to avoid magic strings.
    
    SELECT: User can navigate and select cells
    EDIT: User is actively editing a cell's content
    """
    SELECT = "SELECT"
    EDIT = "EDIT"


class EntryState(Enum):
    """
    Enum for entry widget states to maintain consistency.
    
    NORMAL: Entry widget allows user input
    READONLY: Entry widget is read-only, no direct editing
    """
    NORMAL = "normal"
    READONLY = "readonly"


@dataclass
class StyleConfig:
    """
    Configuration for visual styling to centralize magic values.
    This makes it easy to change colors, borders, and sizing consistently.
    """
    # Color definitions for different cell states
    TABLE_BG = "#cccccc"        # Background color for the table frame
    CELL_NORMAL_BG = "white"    # Normal cell background
    CELL_SELECTED_BG = "#dbeeff" # Selected cell background (light blue)
    CELL_EDITING_BG = "#90EE90"  # Editing cell background (light green)
    
    # Border style configurations
    NORMAL_BORDER = {"relief": "solid", "bd": 1}    # Standard cell border
    SELECTED_BORDER = {"relief": "solid", "bd": 2}  # Highlighted cell border (thicker)
    
    # Cell sizing and spacing properties
    CELL_WIDTH = 12                    # Width of each cell in characters
    CELL_PADDING = {"padx": 1, "pady": 1}  # Padding around each cell