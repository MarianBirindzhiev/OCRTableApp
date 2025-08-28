from utilities import BG_COLOR, FONT, LOGGER_NAME
import tkinter as tk
import logging

logger = logging.getLogger(LOGGER_NAME)

class TableCanvas:

    def __init__(self):
        # Holds reference to app state (e.g. grid size, current cell, cell values)
        self.state = None
        # 2D list of Entry widgets
        self.entries = []
        # Store controller reference for callbacks
        self.controller = None

    def build(self, controller):
        """
        Build the table UI inside the root widget and initialize state and callbacks.
        """
        logger.info("Building TableCanvas UI.")
        self.state = controller.state
        self.controller = controller  # Store controller reference
        self.entries = []

        # Container for scrollable canvas and scrollbars
        container = tk.Frame(controller.root, bg=BG_COLOR)
        container.pack(fill='both', expand=True)
        logger.debug("Created container frame.")

        # Scrollable canvas
        self.canvas = tk.Canvas(container, borderwidth=0, bg=BG_COLOR)
        self.scroll_x = tk.Scrollbar(container, orient="horizontal", command=self.canvas.xview)
        self.scroll_y = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        # Pack the scrollbars and canvas
        self.scroll_x.pack(side="bottom", fill="x")
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        logger.debug("Canvas and scrollbars packed.")

        # Frame inside the canvas for the table cells
        self.table_frame = tk.Frame(self.canvas, bg="#cccccc")
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        logger.debug("Created table_frame inside canvas.")

        # When table size changes, update the scroll region
        self.table_frame.bind("<Configure>", self.update_scroll_region)
        logger.debug("Bound update_scroll_region to <Configure> event.")        

        # Create the initial grid of entries
        self._rebuild(controller.state, controller.callbacks)

    def _rebuild(self, state, callbacks):
        """Rebuild table with enhanced mode-aware bindings"""
        # Clear existing widgets
        for widget in self.table_frame.winfo_children():  # ✅ Fixed: use table_frame
            widget.destroy()
        
        self.entries = []
        
        for r in range(state.rows):  # ✅ Fixed: use state parameter
            row_entries = []
            for c in range(state.cols):  # ✅ Fixed: use state parameter
                e = tk.Entry(
                    self.table_frame, font=FONT, justify='center',  # ✅ Fixed: use table_frame
                    relief='solid', bd=1, width=12,
                    state='readonly'  # ✅ Start in readonly mode for SELECT
                )
                e.grid(row=r, column=c, padx=1, pady=1)
                
                # Set initial content
                if r < len(state.grid_data) and c < len(state.grid_data[r]):  # ✅ Fixed: use state parameter
                    # Temporarily enable to insert content
                    e.config(state='normal')
                    e.insert(0, state.grid_data[r][c])
                    e.config(state='readonly')
                
                # Enhanced event bindings for mode-aware behavior
                e.bind("<Button-1>", lambda event, row=r, col=c: self._handle_cell_click(event, row, col, callbacks))
                e.bind("<FocusIn>", lambda event, row=r, col=c: self._on_focus_in(event, row, col, callbacks))
                e.bind("<FocusOut>", lambda event, row=r, col=c: self._on_focus_out(event, row, col, callbacks))
                e.bind("<KeyPress>", lambda event, row=r, col=c: self._handle_key_press(event, row, col, callbacks))
                e.bind("<KeyRelease>", lambda event, row=r, col=c: callbacks.get("cell_changed", lambda r, c, e: None)(row, col, event))
                
                # Navigation bindings (only work in SELECT mode)
                e.bind("<Up>", lambda event, row=r, col=c: self._navigate_if_select_mode(event, row, col, callbacks, "up"))
                e.bind("<Down>", lambda event, row=r, col=c: self._navigate_if_select_mode(event, row, col, callbacks, "down"))
                e.bind("<Left>", lambda event, row=r, col=c: self._navigate_if_select_mode(event, row, col, callbacks, "left"))
                e.bind("<Right>", lambda event, row=r, col=c: self._navigate_if_select_mode(event, row, col, callbacks, "right"))
                
                row_entries.append(e)
            self.entries.append(row_entries)
        
        # Set initial highlighting
        self.highlight_active_cell()
        logger.debug("Table canvas rebuilt with mode-aware bindings")
            
    def highlight_active_cell(self):
        """Enhanced highlighting that shows both select and edit states"""
        current_pos = self.state.current_pos
        editing_cell = getattr(self.state, 'editing_cell', None)
        interaction_mode = getattr(self.state, 'interaction_mode', 'SELECT')
        
        logger.debug(f"Highlighting - pos: {current_pos}, editing: {editing_cell}, mode: {interaction_mode}")
        
        for r in range(self.state.rows):
            for c in range(self.state.cols):
                if r < len(self.entries) and c < len(self.entries[r]):
                    entry = self.entries[r][c]
                    
                    if (r, c) == editing_cell and interaction_mode == "EDIT":
                        # Green background for edit mode
                        entry.config(bg='#90EE90', relief="solid", bd=2, state='normal')
                    elif (r, c) == current_pos and interaction_mode == "SELECT":
                        # Light blue for selected cell in select mode
                        entry.config(bg='#dbeeff', relief="solid", bd=2, state='readonly')
                    else:
                        # White for normal cells
                        entry.config(bg='white', relief="solid", bd=1, state='readonly')


    def _handle_cell_click(self, event, row, col, callbacks):
        """Handle cell clicks for SELECT/edit mode logic with single click on selected cell"""
        current_mode = getattr(self.state, 'interaction_mode', 'SELECT')
        current_pos = self.state.current_pos
        editing_cell = getattr(self.state, 'editing_cell', None)
        
        logger.debug(f"Cell click: ({row}, {col}), current mode: {current_mode}, current pos: {current_pos}, editing: {editing_cell}")
        
        if current_mode == "SELECT":
            if current_pos == (row, col):
                # Clicking on the already selected cell - enter edit mode
                logger.debug(f"Clicking on already selected cell ({row}, {col}) - entering edit mode")
                callbacks["enter_edit_mode"](row, col)
            else:
                # Clicking on a different cell - just select it
                logger.debug(f"Selecting new cell ({row}, {col})")
                callbacks["select_cell"](row, col)
        
        elif current_mode == "EDIT":
            if editing_cell == (row, col):
                # Clicking on the cell we're already editing - keep focus, do nothing special
                logger.debug(f"Clicking on cell we're already editing ({row}, {col}) - maintaining edit mode")
                pass
            else:
                # Clicking on a different cell while editing - exit edit mode and select new cell
                logger.debug(f"Clicking different cell ({row}, {col}) while editing - exiting edit mode and selecting new cell")
                callbacks["exit_edit_mode"]()
                callbacks["select_cell"](row, col)

    def _handle_key_press(self, event, row, col, callbacks):
        """Handle key presses based on current mode"""
        current_mode = getattr(self.state, 'interaction_mode', 'SELECT')
        
        logger.debug(f"Key press: {event.keysym} in mode: {current_mode}")
        
        if current_mode == "SELECT":
            if event.keysym in ["Delete", "BackSpace"]:
                # In select mode, delete entire cell content
                logger.debug(f"Delete key in select mode - clearing cell ({row}, {col})")
                callbacks["delete_cell_content"](row, col)
                return "break"  # Prevent default behavior
            elif event.keysym in ["Up", "Down", "Left", "Right"]:
                # Arrow keys handled by navigation bindings
                pass
            elif event.keysym in ["Return", "KP_Enter", "space"]:
                # Enter or space key in select mode - enter edit mode
                logger.debug(f"Enter/Space key in select mode - entering edit mode for ({row}, {col})")
                callbacks["enter_edit_mode"](row, col)
                return "break"
            elif len(event.char) == 1 and event.char.isprintable():
                # Any printable character in select mode - enter edit mode and start typing
                logger.debug(f"Typing '{event.char}' in select mode - entering edit mode")
                callbacks["enter_edit_mode"](row, col)
                # Clear current content and insert the new character
                self.controller.root.after_idle(lambda: self._replace_content_and_type(row, col, event.char))
                return "break"
        
        elif current_mode == "EDIT":
            if event.keysym == "Escape":
                # Escape key exits edit mode
                logger.debug("Escape pressed - exiting edit mode")
                callbacks["exit_edit_mode"]()
                return "break"
            elif event.keysym in ["Return", "KP_Enter"]:
                # Enter key exits edit mode and optionally moves to next cell
                logger.debug("Return pressed - exiting edit mode")
                callbacks["exit_edit_mode"]()
                return "break"
            # In edit mode, allow normal key behavior for typing (Delete, Backspace work normally)
    
    def _replace_content_and_type(self, row, col, char):
        """Helper to replace cell content when starting to type in select mode"""
        if (row < len(self.entries) and col < len(self.entries[row])):
            entry = self.entries[row][col]
            if entry['state'] == 'normal':  # Only if in edit mode
                entry.delete(0, tk.END)  # Clear existing content
                entry.insert(0, char)     # Insert the typed character
                entry.icursor(1)          # Position cursor after the character

    def _navigate_if_select_mode(self, event, row, col, callbacks, direction):
        """Only allow navigation if in SELECT mode"""
        current_mode = getattr(self.state, 'interaction_mode', 'SELECT')
        
        if current_mode == "SELECT":
            # Allow navigation
            if direction == "up":
                self._navigate_up(row, col, callbacks)
            elif direction == "down":
                self._navigate_down(row, col, callbacks)
            elif direction == "left":
                self._navigate_left(row, col, callbacks)
            elif direction == "right":
                self._navigate_right(row, col, callbacks)
            return "break"
        else:
            # In EDIT mode, don't intercept navigation keys (let normal text editing work)
            return None

    def _on_focus_in(self, event, row, col, callbacks):
        """Handle focus in - but don't auto-enter edit mode"""
        current_mode = getattr(self.state, 'interaction_mode', 'SELECT')
        
        if current_mode == "SELECT":
            # Just select the cell, don't enter edit mode automatically
            callbacks["select_cell"](row, col)

    def _on_focus_out(self, event, row, col, callbacks):
        """Handle focus out - if in edit mode, exit it"""
        current_mode = getattr(self.state, 'interaction_mode', 'SELECT')
        editing_cell = getattr(self.state, 'editing_cell', None)
        
        if current_mode == "EDIT" and editing_cell == (row, col):
            callbacks["exit_edit_mode"]()
    def _navigate_up(self, row, col, callbacks):
        """Navigate to the cell above if it exists."""
        if row > 0:
            callbacks["select_cell"](row - 1, col)
            self.entries[row - 1][col].focus_set()
            logger.debug(f"Navigated up from ({row}, {col}) to ({row - 1}, {col})")

    def _navigate_down(self, row, col, callbacks):
        """Navigate to the cell below if it exists."""
        if row < self.state.rows - 1:
            callbacks["select_cell"](row + 1, col)
            self.entries[row + 1][col].focus_set()
            logger.debug(f"Navigated down from ({row}, {col}) to ({row + 1}, {col})")

    def _navigate_left(self, row, col, callbacks):
        """Navigate to the cell on the left if it exists."""
        if col > 0:
            callbacks["select_cell"](row, col - 1)
            self.entries[row][col - 1].focus_set()
            logger.debug(f"Navigated left from ({row}, {col}) to ({row}, {col - 1})")

    def _navigate_right(self, row, col, callbacks):
        """Navigate to the cell on the right if it exists."""
        if col < self.state.cols - 1:
            callbacks["select_cell"](row, col + 1)
            self.entries[row][col + 1].focus_set()
            logger.debug(f"Navigated right from ({row}, {col}) to ({row}, {col + 1})")

    def get_entry_value(self, row, col):
        """
        Get the string value from the entry at (row, col).
        """
        value = self.entries[row][col].get()
        logger.debug(f"Retrieved value from entry ({row}, {col}): {value}")
        return value

    def update_scroll_region(self, event=None):
        """
        Adjust the scroll region based on the content size.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        logger.debug("Updated scroll region of the canvas.")