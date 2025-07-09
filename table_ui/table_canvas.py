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
    def build(self, controller):
        """
        Build the table UI inside the root widget and initialize state and callbacks.
        """
        logger.info("Building TableCanvas UI.")
        self.state = controller.state
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

    def _rebuild(self, state=None, callbacks=None):
        """
        Recreate the table grid, e.g. after resize.
        """
        logger.info("Rebuilding table grid.")        
        if state:
            self.state = state
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.entries = []
        logger.debug("Cleared existing table widgets.")

        # Rebuild the grid of Entry widgets
        for r in range(self.state.rows):
            row_entries = []
            for c in range(self.state.cols):
                e = tk.Entry(self.table_frame, width=12, font=FONT, justify="left", relief="solid", bd=1)
                e.grid(row=r, column=c)
                e.insert(0, self.state.get_cell(r, c))
                e.bind("<Button-1>", lambda event, row=r, col=c: callbacks["select_cell"](row, col))
                e.bind("<FocusIn>", lambda event, row=r, col=c: callbacks["start_edit"](row, col))
                e.bind("<KeyRelease>", lambda event, row=r, col=c: callbacks["finish_edit"](row, col))
                
                # Bind arrow keys for navigation
                e.bind("<Up>", lambda event, row=r, col=c: self._navigate_up(row, col, callbacks))
                e.bind("<Down>", lambda event, row=r, col=c: self._navigate_down(row, col, callbacks))
                e.bind("<Left>", lambda event, row=r, col=c: self._navigate_left(row, col, callbacks))
                e.bind("<Right>", lambda event, row=r, col=c: self._navigate_right(row, col, callbacks))
                
                row_entries.append(e)
                logger.debug(f"Entry ({r}, {c}) initialized with value: '{self.state.get_cell(r, c)}'") 
            self.entries.append(row_entries)

        logger.info(f"Table grid rebuilt with {self.state.rows} rows and {self.state.cols} columns.")
        self.highlight_active_cell()
        self.update_scroll_region()

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

    def highlight_active_cell(self):
        """
        Highlight the currently selected cell in light blue.
        """
        logger.debug(f"Highlighting active cell at {self.state.current_pos}")        
        for r in range(self.state.rows):
            for c in range(self.state.cols):
                color = '#dbeeff' if (r, c) == self.state.current_pos else 'white'
                self.entries[r][c].config(bg=color)

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
