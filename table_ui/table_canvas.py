from utilities import BG_COLOR, FONT, LOGGER_NAME
from .table_ui_utils import InteractionMode, EntryState, StyleConfig, CellEventHandler, CanvasNavigationHandler

import tkinter as tk
import logging
import time
from typing import Optional, Callable, Dict, Any, Tuple, List

# Initialize logger for this module
logger = logging.getLogger(LOGGER_NAME)


class TableCanvas:
    """
    Main table canvas class with improved separation of concerns.
    
    This class manages the overall table UI, including:
    - Creating and managing the scrollable canvas
    - Building the grid of Entry widgets
    - Coordinating event handling and styling
    - Providing an interface between the UI and the controller
    
    The class follows the single responsibility principle by delegating
    specific tasks to helper classes (CellEventHandler, NavigationHandler).
    """
    
    def __init__(self):
        """
        Initialize the TableCanvas with default empty state.
        
        Components are created but not built until build() is called.
        """
        logger.debug("Initializing TableCanvas instance")
        
        # Core state references (set during build())
        self.state = None                           # Reference to application state
        self.entries: List[List[tk.Entry]] = []     # 2D list of Entry widgets
        self.controller = None                      # Reference to controller for callbacks
        
        # Configuration and helper objects
        self.style_config = StyleConfig()           # Styling configuration
        logger.debug(f"StyleConfig created with cell_width={self.style_config.CELL_WIDTH}")
        
        self.navigation_handler = CanvasNavigationHandler(self)  # Navigation logic handler
        logger.debug("CanvasNavigationHandler initialized")
        
        # UI Components (created during build())
        self.canvas: Optional[tk.Canvas] = None     # Main scrollable canvas
        self.scroll_x: Optional[tk.Scrollbar] = None # Horizontal scrollbar
        self.scroll_y: Optional[tk.Scrollbar] = None # Vertical scrollbar
        self.table_frame: Optional[tk.Frame] = None  # Frame containing the grid
        
        logger.info("TableCanvas initialization completed")
    
    def build(self, controller) -> None:
        """
        Build the table UI inside the root widget.
        
        This is the main entry point for creating the table interface.
        It sets up the scrollable container and builds the initial grid.
        
        Args:
            controller: The controller object containing state and callbacks
        """
        build_start_time = time.perf_counter()
        logger.info("Building TableCanvas UI.")
        
        # Store references to controller and state
        self.state = controller.state
        self.controller = controller
        self.entries = []
        
        logger.debug(f"Controller state: rows={getattr(controller.state, 'rows', 'N/A')}, "
                    f"cols={getattr(controller.state, 'cols', 'N/A')}")
        logger.debug(f"Available callbacks: {list(controller.callbacks.keys()) if hasattr(controller, 'callbacks') else 'No callbacks'}")
        
        # Create the UI structure
        ui_start_time = time.perf_counter()
        self._create_ui_components(controller.root)
        ui_duration = time.perf_counter() - ui_start_time
        logger.debug(f"UI components creation took {ui_duration:.3f} seconds")
        
        # Build the table grid with event bindings
        grid_start_time = time.perf_counter()
        self.rebuild_table(controller.callbacks)
        grid_duration = time.perf_counter() - grid_start_time
        logger.debug(f"Table grid creation took {grid_duration:.3f} seconds")
        
        build_duration = time.perf_counter() - build_start_time
        logger.info(f"TableCanvas build completed in {build_duration:.3f} seconds")
    
    def _create_ui_components(self, root: tk.Widget) -> None:
        """
        Create and setup the scrollable UI components.
        
        Creates a container with a scrollable canvas and scrollbars,
        then adds a frame inside the canvas to hold the table cells.
        
        Args:
            root: Parent widget to contain the table
        """
        logger.debug("Starting UI components creation")
        
        # Create main container frame for the entire table UI
        container = tk.Frame(root, bg=BG_COLOR)
        container.pack(fill='both', expand=True)
        logger.debug(f"Main container created with background color: {BG_COLOR}")
        
        # Create scrollable canvas for the table content
        self.canvas = tk.Canvas(container, borderwidth=0, bg=BG_COLOR)
        logger.debug("Scrollable canvas created")
        
        # Create scrollbars linked to the canvas
        self.scroll_x = tk.Scrollbar(container, orient="horizontal", command=self.canvas.xview)
        self.scroll_y = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        logger.debug("Scrollbars created (horizontal and vertical)")
        
        # Configure canvas to work with scrollbars
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        logger.debug("Canvas configured with scrollbar commands")
        
        # Pack scrollbars and canvas in the container
        self.scroll_x.pack(side="bottom", fill="x")     # Horizontal scrollbar at bottom
        self.scroll_y.pack(side="right", fill="y")      # Vertical scrollbar at right
        self.canvas.pack(side="left", fill="both", expand=True)  # Canvas fills remaining space
        logger.debug("Scrollbars and canvas packed in container")
        
        # Create frame inside canvas to hold the actual table cells
        self.table_frame = tk.Frame(self.canvas, bg=self.style_config.TABLE_BG)
        logger.debug(f"Table frame created with background: {self.style_config.TABLE_BG}")
        
        # Add the table frame to the canvas as a window
        canvas_window = self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        logger.debug(f"Table frame added to canvas as window (ID: {canvas_window})")
        
        # Bind event to update scroll region when table size changes
        self.table_frame.bind("<Configure>", self._update_scroll_region)
        logger.debug("Configure event bound to table frame for scroll region updates")
        
        logger.debug("UI components created successfully.")
    
    def rebuild_table(self, callbacks: Dict[str, Callable]) -> None:
        """
        Rebuild the table with cells and event handlers.
        
        This method completely recreates the table grid, typically called
        when the table size changes or when initially building the table.
        
        Args:
            callbacks: Dictionary of callback functions for various events
        """
        rebuild_start_time = time.perf_counter()
        rows = self.get_row_count()
        cols = self.get_col_count()
        total_cells = rows * cols
        
        logger.info(f"Starting table rebuild: {rows}x{cols} ({total_cells} cells)")
        logger.debug(f"Available callbacks for rebuild: {list(callbacks.keys())}")
        
        # Remove all existing widgets and clear the entries list
        clear_start_time = time.perf_counter()
        self._clear_existing_widgets()
        clear_duration = time.perf_counter() - clear_start_time
        logger.debug(f"Widget clearing took {clear_duration:.3f} seconds")
        
        # Create new grid of Entry widgets
        grid_start_time = time.perf_counter()
        self._create_cell_grid(callbacks)
        grid_duration = time.perf_counter() - grid_start_time
        logger.debug(f"Cell grid creation took {grid_duration:.3f} seconds")
        
        # Apply initial highlighting based on current state
        highlight_start_time = time.perf_counter()
        self.highlight_active_cell()
        highlight_duration = time.perf_counter() - highlight_start_time
        logger.debug(f"Initial highlighting took {highlight_duration:.3f} seconds")
        
        rebuild_duration = time.perf_counter() - rebuild_start_time
        logger.info(f"Table rebuild completed in {rebuild_duration:.3f} seconds for {total_cells} cells")
        
        if rebuild_duration > 1.0:  # Warn if rebuild takes more than 1 second
            logger.warning(f"Slow table rebuild detected: {rebuild_duration:.3f}s for {rows}x{cols} table")
    
    def _clear_existing_widgets(self) -> None:
        """
        Clear all existing widgets from the table frame.
        
        This is called before rebuilding the table to ensure a clean slate.
        All Entry widgets are destroyed and the entries list is reset.
        """
        widget_count = 0
        if self.table_frame:
            # Count widgets before destroying
            widgets = self.table_frame.winfo_children()
            widget_count = len(widgets)
            logger.debug(f"Destroying {widget_count} existing widgets")
            
            # Destroy all child widgets in the table frame
            for widget in widgets:
                widget.destroy()
        
        # Reset the entries list
        previous_entry_count = sum(len(row) for row in self.entries) if self.entries else 0
        self.entries = []
        
        logger.debug(f"Cleared {widget_count} widgets and {previous_entry_count} entry references")
    
    def _create_cell_grid(self, callbacks: Dict[str, Callable]) -> None:
        """
        Create the grid of Entry widgets.
        
        This method creates a 2D grid of Entry widgets based on the current
        state dimensions, populates them with data, and binds event handlers.
        
        Args:
            callbacks: Dictionary of callback functions for events
        """
        rows = self.get_row_count()
        cols = self.get_col_count()
        
        logger.debug(f"Creating cell grid: {rows} rows x {cols} columns")
        
        # Create entries for each row and column
        for row in range(rows):
            row_start_time = time.perf_counter()
            row_entries = []
            
            for col in range(cols):
                # Create individual cell entry with events and styling
                entry = self._create_cell_entry(row, col, callbacks)
                row_entries.append(entry)
            
            self.entries.append(row_entries)
            
            # Log progress for large tables
            if rows > 50 and (row + 1) % 10 == 0:
                row_duration = time.perf_counter() - row_start_time
                logger.debug(f"Created row {row + 1}/{rows} ({cols} cells) in {row_duration:.3f}s")
        
        logger.debug(f"Cell grid creation completed: {len(self.entries)} rows with {sum(len(row) for row in self.entries)} total cells")
    
    def _create_cell_entry(self, row: int, col: int, callbacks: Dict[str, Callable]) -> tk.Entry:
        """
        Create a single cell Entry widget with proper configuration and bindings.
        
        This method creates one Entry widget, configures its appearance,
        sets its initial content, and binds all necessary events.
        
        Args:
            row: Row index for this cell
            col: Column index for this cell
            callbacks: Dictionary of callback functions
            
        Returns:
            Configured Entry widget
        """
        logger.debug(f"Creating cell entry at position ({row}, {col})")
        
        try:
            # Create Entry widget with standard configuration
            entry = tk.Entry(
                self.table_frame,                           # Parent frame
                font=FONT,                                  # Font from utilities
                justify='center',                           # Center-align text
                width=self.style_config.CELL_WIDTH,         # Width in characters
                state=EntryState.READONLY.value,            # Start in readonly mode
                **self.style_config.NORMAL_BORDER          # Apply normal border style
            )
            logger.debug(f"Entry widget created for ({row}, {col}) with width={self.style_config.CELL_WIDTH}")
            
            # Position the entry in the grid
            entry.grid(row=row, column=col, **self.style_config.CELL_PADDING)
            logger.debug(f"Entry positioned in grid at ({row}, {col}) with padding={self.style_config.CELL_PADDING}")
            
            # Set the initial content from the data model
            self._set_initial_cell_content(entry, row, col)
            
            # Bind all event handlers for this cell
            self._bind_cell_events(entry, row, col, callbacks)
            
            logger.debug(f"Cell entry creation completed for ({row}, {col})")
            return entry
            
        except Exception as e:
            logger.error(f"Failed to create cell entry at ({row}, {col}): {e}")
            raise
    
    def _set_initial_cell_content(self, entry: tk.Entry, row: int, col: int) -> None:
        """
        Set initial content for a cell Entry widget.
        
        Retrieves the content from the state's grid_data and populates
        the Entry widget. Temporarily enables the widget to allow content insertion.
        
        Args:
            entry: Entry widget to populate
            row: Row index in the grid_data
            col: Column index in the grid_data
        """
        # Check if this position has data in the grid
        if (row < len(self.state.grid_data) and 
            col < len(self.state.grid_data[row])):
            
            content = self.state.grid_data[row][col]
            logger.debug(f"Setting initial content for ({row}, {col}): '{content}'")
            
            # Temporarily enable entry to insert content
            entry.config(state=EntryState.NORMAL.value)
            entry.insert(0, content)
            
            # Return to readonly state
            entry.config(state=EntryState.READONLY.value)
            
            logger.debug(f"Content set and entry returned to readonly state for ({row}, {col})")
        else:
            logger.debug(f"No initial content available for position ({row}, {col})")
    
    def _bind_cell_events(self, entry: tk.Entry, row: int, col: int, callbacks: Dict[str, Callable]) -> None:
        """
        Bind all events for a cell Entry widget.
        
        Creates a CellEventHandler for this specific cell and binds
        all necessary events including mouse clicks, focus changes,
        key presses, and navigation.
        
        Args:
            entry: Entry widget to bind events to
            row: Row index of this cell
            col: Column index of this cell
            callbacks: Dictionary of callback functions
        """
        logger.debug(f"Binding events for cell ({row}, {col})")
        
        try:
            # Create event handler for this specific cell
            handler = CellEventHandler(self, row, col)
            logger.debug(f"CellEventHandler created for ({row}, {col})")
            
            # Bind basic interaction events
            entry.bind("<Button-1>", lambda e: handler.handle_click(e))        # Left mouse click
            entry.bind("<FocusIn>", lambda e: handler.handle_focus_in(e))       # Gained keyboard focus
            entry.bind("<FocusOut>", lambda e: handler.handle_focus_out(e))     # Lost keyboard focus
            entry.bind("<KeyPress>", lambda e: handler.handle_key_press(e))     # Key pressed
            logger.debug(f"Basic interaction events bound for ({row}, {col})")
            
            # Bind key release event to controller callback (for real-time updates)
            entry.bind("<KeyRelease>", lambda e, r=row, c=col: 
                      callbacks.get("cell_changed", lambda r, c, e: None)(r, c, e))
            logger.debug(f"KeyRelease event bound for ({row}, {col}) with callback: {'cell_changed' in callbacks}")
            
            # Bind navigation events (arrow keys)
            navigation_bindings = {
                "<Up>": "up", 
                "<Down>": "down", 
                "<Left>": "left", 
                "<Right>": "right"
            }
            
            # Bind each navigation key to the navigation handler
            for key, direction in navigation_bindings.items():
                entry.bind(key, lambda e, d=direction: self._handle_navigation(row, col, d))
            
            logger.debug(f"Navigation events bound for ({row}, {col}): {list(navigation_bindings.keys())}")
            logger.debug(f"Event binding completed for cell ({row}, {col})")
            
        except Exception as e:
            logger.error(f"Failed to bind events for cell ({row}, {col}): {e}")
            raise
    
    def _handle_navigation(self, row: int, col: int, direction: str) -> Optional[str]:
        """
        Handle navigation key presses.
        
        Delegates to the NavigationHandler and returns 'break' if navigation
        occurred to prevent default Entry widget behavior.
        
        Args:
            row: Current row position
            col: Current column position
            direction: Direction to navigate ('up', 'down', 'left', 'right')
            
        Returns:
            'break' if navigation occurred, None otherwise
        """
        logger.debug(f"Navigation requested from ({row}, {col}) direction: {direction}")
        
        try:
            if self.navigation_handler.navigate(row, col, direction):
                logger.debug(f"Navigation successful from ({row}, {col}) {direction}")
                return "break"  # Prevent default arrow key behavior in Entry widget
            else:
                logger.debug(f"Navigation blocked from ({row}, {col}) {direction} (boundary or invalid)")
                return None
        except Exception as e:
            logger.error(f"Navigation error from ({row}, {col}) {direction}: {e}")
            return None
    
    def highlight_active_cell(self) -> None:
        """
        Update cell highlighting based on current application state.
        
        This method reads the current state (position, mode, editing cell)
        and updates the visual appearance of all cells accordingly.
        Different cells get different styling based on their state:
        - Editing cell: green background, normal state
        - Selected cell: blue background, readonly state  
        - Normal cells: white background, readonly state
        """
        highlight_start_time = time.perf_counter()
        
        # Get current state information
        current_pos = self.get_current_position()
        editing_cell = self.get_editing_cell()
        interaction_mode = self.get_interaction_mode()
        
        logger.debug(f"Highlighting - pos: {current_pos}, editing: {editing_cell}, mode: {interaction_mode}")
        
        cells_updated = 0
        rows = self.get_row_count()
        cols = self.get_col_count()
        
        # Update appearance for all cells
        for row in range(rows):
            for col in range(cols):
                if self._is_valid_entry_position(row, col):
                    self._update_cell_appearance(row, col, current_pos, editing_cell, interaction_mode)
                    cells_updated += 1
        
        highlight_duration = time.perf_counter() - highlight_start_time
        logger.debug(f"Highlighting completed: {cells_updated} cells updated in {highlight_duration:.3f} seconds")
        
        if highlight_duration > 0.5:  # Warn if highlighting takes more than 0.5 seconds
            logger.warning(f"Slow highlighting operation: {highlight_duration:.3f}s for {rows}x{cols} table")
    
    def _is_valid_entry_position(self, row: int, col: int) -> bool:
        """
        Check if the Entry widget position is valid and exists.
        
        Verifies that the row/col indices are within bounds and that
        the Entry widget at that position actually exists.
        
        Args:
            row: Row index to check
            col: Column index to check
            
        Returns:
            True if position is valid and Entry exists, False otherwise
        """
        is_valid = (row < len(self.entries) and 
                   col < len(self.entries[row]) and 
                   self.entries[row][col] is not None)
        
        if not is_valid:
            logger.debug(f"Invalid entry position: ({row}, {col}) - "
                        f"entries_len={len(self.entries)}, "
                        f"row_len={len(self.entries[row]) if row < len(self.entries) else 'N/A'}")
        
        return is_valid
    
    def _update_cell_appearance(self, row: int, col: int, current_pos: Tuple[int, int], 
                              editing_cell: Optional[Tuple[int, int]], mode: InteractionMode) -> None:
        """
        Update the visual appearance of a single cell.
        
        Applies appropriate styling based on the cell's state:
        - If this is the editing cell in EDIT mode: green background, editable
        - If this is the selected cell in SELECT mode: blue background, readonly
        - Otherwise: white background, readonly
        
        Args:
            row: Row index of the cell
            col: Column index of the cell
            current_pos: Currently selected position
            editing_cell: Currently editing position (if any)
            mode: Current interaction mode
        """
        entry = self.entries[row][col]
        
        try:
            if (row, col) == editing_cell and mode == InteractionMode.EDIT:
                # Cell is being edited: green background, normal state for input
                entry.config(
                    bg=self.style_config.CELL_EDITING_BG,
                    state=EntryState.NORMAL.value,
                    **self.style_config.SELECTED_BORDER
                )
                logger.debug(f"Cell ({row}, {col}) styled as EDITING")
                
            elif (row, col) == current_pos and mode == InteractionMode.SELECT:
                # Cell is selected but not editing: blue background, readonly
                entry.config(
                    bg=self.style_config.CELL_SELECTED_BG,
                    state=EntryState.READONLY.value,
                    **self.style_config.SELECTED_BORDER
                )
                logger.debug(f"Cell ({row}, {col}) styled as SELECTED")
                
            else:
                # Normal cell: white background, readonly
                entry.config(
                    bg=self.style_config.CELL_NORMAL_BG,
                    state=EntryState.READONLY.value,
                    **self.style_config.NORMAL_BORDER
                )
                # Only log this for cells that were previously highlighted to reduce noise
                if (row, col) == current_pos or (row, col) == editing_cell:
                    logger.debug(f"Cell ({row}, {col}) styled as NORMAL")
                    
        except Exception as e:
            logger.error(f"Failed to update appearance for cell ({row}, {col}): {e}")
    
    def _update_scroll_region(self, event=None) -> None:
        """
        Update scroll region based on the current content size.
        
        This is called whenever the table frame is resized to ensure
        the scrollbars properly reflect the scrollable area.
        
        Args:
            event: Configure event (unused but required by binding)
        """
        if self.canvas:
            try:
                # Get current scroll region before update
                old_region = self.canvas.cget('scrollregion')
                
                # Update the scrollable region to match the content size
                bbox = self.canvas.bbox("all")
                self.canvas.configure(scrollregion=bbox)
                
                new_region = self.canvas.cget('scrollregion')
                
                if old_region != new_region:
                    logger.debug(f"Scroll region updated: {old_region} -> {new_region}")
                    logger.debug(f"Canvas bbox: {bbox}")
                else:
                    logger.debug("Scroll region update called but no change needed")
                    
            except Exception as e:
                logger.error(f"Error updating scroll region: {e}")
    
    # State access methods - these provide a clean interface to state information
    
    def get_interaction_mode(self) -> InteractionMode:
        """
        Get current interaction mode from the application state.
        
        Returns:
            Current InteractionMode (SELECT or EDIT)
        """
        mode_str = getattr(self.state, 'interaction_mode', 'SELECT')
        mode = InteractionMode(mode_str)
        logger.debug(f"Retrieved interaction mode: {mode}")
        return mode
    
    def get_current_position(self) -> Tuple[int, int]:
        """
        Get current cell position from the application state.
        
        Returns:
            Tuple of (row, col) representing the current position
        """
        pos = getattr(self.state, 'current_pos', (0, 0))
        logger.debug(f"Retrieved current position: {pos}")
        return pos
    
    def get_editing_cell(self) -> Optional[Tuple[int, int]]:
        """
        Get currently editing cell position from the application state.
        
        Returns:
            Tuple of (row, col) if editing, None if not in edit mode
        """
        editing = getattr(self.state, 'editing_cell', None)
        logger.debug(f"Retrieved editing cell: {editing}")
        return editing
    
    def get_row_count(self) -> int:
        """
        Get number of rows in the table.
        
        Returns:
            Number of rows in the current table
        """
        rows = getattr(self.state, 'rows', 0)
        logger.debug(f"Retrieved row count: {rows}")
        return rows
    
    def get_col_count(self) -> int:
        """
        Get number of columns in the table.
        
        Returns:
            Number of columns in the current table
        """
        cols = getattr(self.state, 'cols', 0)
        logger.debug(f"Retrieved column count: {cols}")
        return cols
    
    # Controller callback methods - these provide interface to controller functionality
    
    def select_cell(self, row: int, col: int) -> None:
        """
        Select a cell via controller callback.
        
        This method delegates to the controller's select_cell callback,
        which updates the application state and triggers any necessary updates.
        
        Args:
            row: Row index to select
            col: Column index to select
        """
        logger.info(f"Selecting cell ({row}, {col})")
        
        if self.controller and hasattr(self.controller, 'callbacks'):
            callback = self.controller.callbacks.get("select_cell")
            if callback:
                try:
                    callback(row, col)
                    logger.debug(f"select_cell callback executed successfully for ({row}, {col})")
                except Exception as e:
                    logger.error(f"Error in select_cell callback for ({row}, {col}): {e}")
            else:
                logger.warning("select_cell callback not found")
        else:
            logger.error("Controller or callbacks not available for select_cell")
    
    def enter_edit_mode(self, row: int, col: int) -> None:
        """
        Enter edit mode for a specific cell via controller callback.
        
        Args:
            row: Row index of cell to edit
            col: Column index of cell to edit
        """
        logger.info(f"Entering edit mode for cell ({row}, {col})")
        
        if self.controller and hasattr(self.controller, 'callbacks'):
            callback = self.controller.callbacks.get("enter_edit_mode")
            if callback:
                try:
                    callback(row, col)
                    logger.debug(f"enter_edit_mode callback executed successfully for ({row}, {col})")
                except Exception as e:
                    logger.error(f"Error in enter_edit_mode callback for ({row}, {col}): {e}")
            else:
                logger.warning("enter_edit_mode callback not found")
        else:
            logger.error("Controller or callbacks not available for enter_edit_mode")
    
    def exit_edit_mode(self) -> None:
        """
        Exit edit mode via controller callback.
        
        This saves any changes and returns to SELECT mode.
        """
        logger.info("Exiting edit mode")
        
        if self.controller and hasattr(self.controller, 'callbacks'):
            callback = self.controller.callbacks.get("exit_edit_mode")
            if callback:
                try:
                    callback()
                    logger.debug("exit_edit_mode callback executed successfully")
                except Exception as e:
                    logger.error(f"Error in exit_edit_mode callback: {e}")
            else:
                logger.warning("exit_edit_mode callback not found")
        else:
            logger.error("Controller or callbacks not available for exit_edit_mode")
    
    def delete_cell_content(self, row: int, col: int) -> None:
        """
        Delete cell content via controller callback.
        
        Args:
            row: Row index of cell to clear
            col: Column index of cell to clear
        """
        logger.info(f"Deleting content from cell ({row}, {col})")
        
        if self.controller and hasattr(self.controller, 'callbacks'):
            callback = self.controller.callbacks.get("delete_cell_content")
            if callback:
                try:
                    callback(row, col)
                    logger.debug(f"delete_cell_content callback executed successfully for ({row}, {col})")
                except Exception as e:
                    logger.error(f"Error in delete_cell_content callback for ({row}, {col}): {e}")
            else:
                logger.warning("delete_cell_content callback not found")
        else:
            logger.error("Controller or callbacks not available for delete_cell_content")
    
    def focus_cell(self, row: int, col: int) -> None:
        """
        Set keyboard focus to a specific cell.
        
        This is used by navigation to ensure the newly selected cell
        receives keyboard focus for further input.
        
        Args:
            row: Row index of cell to focus
            col: Column index of cell to focus
        """
        logger.debug(f"Setting focus to cell ({row}, {col})")
        
        if self._is_valid_entry_position(row, col):
            try:
                self.entries[row][col].focus_set()
                logger.debug(f"Focus successfully set to cell ({row}, {col})")
            except Exception as e:
                logger.error(f"Failed to set focus to cell ({row}, {col}): {e}")
        else:
            logger.warning(f"Cannot set focus to invalid cell position ({row}, {col})")
    
    def replace_content_and_type(self, row: int, col: int, char: str) -> None:
        """
        Replace cell content when starting to type in SELECT mode.
        
        This is called when the user types a printable character while
        in SELECT mode, which should enter EDIT mode and replace the
        cell content with the typed character.
        
        Args:
            row: Row index of cell to modify
            col: Column index of cell to modify
            char: Character that was typed
        """
        logger.debug(f"Replacing content in cell ({row}, {col}) with character: '{char}'")
        
        if self._is_valid_entry_position(row, col):
            entry = self.entries[row][col]
            # Only proceed if the entry is in normal (editable) state
            if entry['state'] == EntryState.NORMAL.value:
                logger.debug(f"Entry at ({row}, {col}) is editable, scheduling content replacement")
                # Use after_idle to ensure the edit mode transition is complete
                self.controller.root.after_idle(lambda: self._do_replace_content(entry, char))
            else:
                logger.warning(f"Entry at ({row}, {col}) is not editable (state: {entry['state']})")
        else:
            logger.warning(f"Cannot replace content at invalid position ({row}, {col})")
    
    def _do_replace_content(self, entry: tk.Entry, char: str) -> None:
        """
        Perform the actual content replacement operation.
        
        This helper method does the actual work of clearing the entry
        and inserting the new character, then positioning the cursor.
        
        Args:
            entry: Entry widget to modify
            char: Character to insert
        """
        try:
            old_content = entry.get()
            entry.delete(0, tk.END)  # Clear all existing content
            entry.insert(0, char)    # Insert the new character
            entry.icursor(1)         # Position cursor after the character
            
            logger.debug(f"Content replacement completed: '{old_content}' -> '{char}', cursor at position 1")
            
        except Exception as e:
            logger.error(f"Failed to replace content with '{char}': {e}")
    
    def get_entry_value(self, row: int, col: int) -> str:
        """
        Get the string value from the Entry widget at the specified position.
        
        This method provides access to the current content of any cell
        for reading or validation purposes.
        
        Args:
            row: Row index of cell to read
            col: Column index of cell to read
            
        Returns:
            String content of the cell, or empty string if invalid position
        """
        if self._is_valid_entry_position(row, col):
            try:
                value = self.entries[row][col].get()
                logger.debug(f"Retrieved value from entry ({row}, {col}): '{value}'")
                return value
            except Exception as e:
                logger.error(f"Failed to get value from entry ({row}, {col}): {e}")
                return ""
        else:
            logger.warning(f"Cannot get value from invalid position ({row}, {col})")
            return ""