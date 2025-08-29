from .canvas_config import InteractionMode
from utilities import LOGGER_NAME

import logging
from typing import Optional


logger = logging.getLogger(LOGGER_NAME)


class CellEventHandler:
    """
    Handles cell-specific events and interactions.
    
    This class encapsulates all the event handling logic for individual cells,
    including clicks, key presses, and focus changes. Each cell gets its own
    instance of this handler with its specific row/column coordinates.
    """

    def __init__(self, table_canvas, row: int, col: int):
        """
        Initialize the event handler for a specific cell.
        
        Args:
            table_canvas: Reference to the parent TableCanvas instance
            row: Row index of this cell (0-based)
            col: Column index of this cell (0-based)
        """
        self.table_canvas = table_canvas
        self.row = row
        self.col = col
    
    def handle_click(self, event) -> None:
        """
        Handle cell click events based on current interaction mode.
        
        In SELECT mode:
        - Clicking the selected cell enters EDIT mode
        - Clicking a different cell selects it
        
        In EDIT mode:
        - Clicking a different cell exits EDIT mode and selects the new cell
        - Clicking the same cell does nothing (stays in EDIT mode)
        
        Args:
            event: Tkinter event object (unused but required by binding)
        """
        # Get current state information
        current_mode = self.table_canvas.get_interaction_mode()
        current_pos = self.table_canvas.get_current_position()
        editing_cell = self.table_canvas.get_editing_cell()
        
        logger.debug(f"Cell click: ({self.row}, {self.col}), mode: {current_mode}")
        
        if current_mode == InteractionMode.SELECT:
            if current_pos == (self.row, self.col):
                # Double-click behavior: clicking selected cell enters edit mode
                self.table_canvas.enter_edit_mode(self.row, self.col)
            else:
                # Single-click behavior: select the clicked cell
                self.table_canvas.select_cell(self.row, self.col)
        
        elif current_mode == InteractionMode.EDIT:
            if editing_cell != (self.row, self.col):
                # Clicking different cell while editing: exit edit mode and select new cell
                self.table_canvas.exit_edit_mode()
                self.table_canvas.select_cell(self.row, self.col)
            # If clicking the same cell being edited, do nothing (maintain edit mode)
    
    def handle_key_press(self, event) -> Optional[str]:
        """
        Handle key press events based on current interaction mode.
        
        Returns 'break' to prevent default Tkinter behavior for certain keys,
        or None to allow normal processing.
        
        Args:
            event: Tkinter KeyPress event containing key information
            
        Returns:
            'break' to stop event propagation, None to continue normal processing
        """
        current_mode = self.table_canvas.get_interaction_mode()
        
        logger.debug(f"Key press: {event.keysym} in mode: {current_mode}")
        
        # Delegate to mode-specific handlers
        if current_mode == InteractionMode.SELECT:
            return self._handle_select_mode_keys(event)
        elif current_mode == InteractionMode.EDIT:
            return self._handle_edit_mode_keys(event)
        
        return None
    
    def _handle_select_mode_keys(self, event) -> Optional[str]:
        """
        Handle key presses when in SELECT mode.
        
        SELECT mode key behaviors:
        - Delete/Backspace: Clear cell content
        - Enter/Space: Enter edit mode
        - Printable characters: Enter edit mode and start typing
        
        Args:
            event: Tkinter KeyPress event
            
        Returns:
            'break' to prevent default behavior, None otherwise
        """
        if event.keysym in ["Delete", "BackSpace"]:
            # Delete or Backspace: clear the entire cell content
            self.table_canvas.delete_cell_content(self.row, self.col)
            return "break"  # Prevent default delete behavior
        
        elif event.keysym in ["Return", "KP_Enter", "space"]:
            # Enter or Space: enter edit mode for this cell
            self.table_canvas.enter_edit_mode(self.row, self.col)
            return "break"  # Prevent default enter behavior
        
        elif len(event.char) == 1 and event.char.isprintable():
            # Any printable character: enter edit mode and replace content with typed character
            self.table_canvas.enter_edit_mode(self.row, self.col)
            self.table_canvas.replace_content_and_type(self.row, self.col, event.char)
            return "break"  # Prevent default character input
        
        return None  # Allow default behavior for other keys (like arrow keys)
    
    def _handle_edit_mode_keys(self, event) -> Optional[str]:
        """
        Handle key presses when in EDIT mode.
        
        EDIT mode key behaviors:
        - Escape: Exit edit mode without saving
        - Enter: Exit edit mode and save changes
        - Other keys: Allow normal text editing
        
        Args:
            event: Tkinter KeyPress event
            
        Returns:
            'break' to prevent default behavior, None otherwise
        """
        if event.keysym == "Escape":
            # Escape: exit edit mode (changes are auto-saved via command pattern)
            self.table_canvas.exit_edit_mode()
            return "break"
        
        elif event.keysym in ["Return", "KP_Enter"]:
            # Enter: confirm edit and exit edit mode
            self.table_canvas.exit_edit_mode()
            return "break"
        
        # For all other keys in edit mode, allow normal text editing behavior
        return None
    
    def handle_focus_in(self, event) -> None:
        """
        Handle focus in events when a cell gains keyboard focus.
        
        In SELECT mode, gaining focus automatically selects the cell.
        In EDIT mode, focus changes are handled by the edit mode logic.
        
        Args:
            event: Tkinter FocusIn event (unused but required)
        """
        if self.table_canvas.get_interaction_mode() == InteractionMode.SELECT:
            # In select mode, focus implies selection
            self.table_canvas.select_cell(self.row, self.col)
    
    def handle_focus_out(self, event) -> None:
        """
        Handle focus out events when a cell loses keyboard focus.
        
        If we're in EDIT mode and this is the cell being edited,
        losing focus should exit edit mode to save changes.
        
        Args:
            event: Tkinter FocusOut event (unused but required)
        """
        current_mode = self.table_canvas.get_interaction_mode()
        editing_cell = self.table_canvas.get_editing_cell()
        
        # If we're editing this cell and it loses focus, exit edit mode
        if current_mode == InteractionMode.EDIT and editing_cell == (self.row, self.col):
            self.table_canvas.exit_edit_mode()

