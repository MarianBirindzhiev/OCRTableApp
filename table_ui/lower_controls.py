from utilities import BG_COLOR, BUTTON_COLOR, BUTTON_HIGHLIGHT, FONT, LOGGER_NAME

import tkinter as tk
import logging

logger = logging.getLogger(LOGGER_NAME)

class LowerControls:
    def __init__(self, state):
        # Store reference to application state (used to get initial rows/cols)
        self.state = state
        logger.debug("LowerControls initialized with state: %dx%d", state.rows, state.cols)

    def build(self, root, callbacks):
        """
        Build the resize controls UI and attach it to the root window.

        Parameters:
        - root: the parent tkinter widget
        - callbacks: a dictionary of callback functions for UI actions
        """
        logger.info("Building lower controls UI.")
        frame = tk.Frame(root, bg=BG_COLOR)
        frame.pack(pady=4)

        for text, command in [
            ("Clear Data", callbacks["clear_all_data"]),
            ("Insert Row", callbacks["insert_row"]),
            ("Insert Column", callbacks["insert_col"]),
        ]:
            logger.debug(f"Creating action button: {text}")            
            tk.Button(
                frame, text=text, command=command,
                font=FONT, bg=BUTTON_COLOR,
                activebackground=BUTTON_HIGHLIGHT,
                relief="groove", padx=12, pady=6
            ).pack(side='left', padx=4)

        # Row input
        tk.Label(frame, text="Rows:", font=FONT, bg=BG_COLOR).pack(side='left', padx=4)
        self.rows_entry = tk.Entry(frame, width=5, font=FONT)
        self.rows_entry.insert(0, str(self.state.rows)) # Pre-fill with current value
        self.rows_entry.pack(side='left')
        logger.debug("Row entry initialized with value: %d", self.state.rows)        

        # Column input
        tk.Label(frame, text="Cols:", font=FONT, bg=BG_COLOR).pack(side='left', padx=4)
        self.cols_entry = tk.Entry(frame, width=5, font=FONT)
        self.cols_entry.insert(0, str(self.state.cols)) # Pre-fill with current value
        self.cols_entry.pack(side='left')
        logger.debug("Column entry initialized with value: %d", self.state.cols)        

        # Apply size button
        tk.Button(
            frame, text="Apply Size", command=callbacks["apply_size"],
            font=FONT, bg=BUTTON_COLOR,
            activebackground=BUTTON_HIGHLIGHT,
            relief="groove", padx=12, pady=4
        ).pack(side='left', padx=10)
        logger.info("Resize controls UI built.")      

    def get_dimensions(self):
        """
        Read the row and column values from the entry fields.

        Returns:
        - tuple of (rows, cols) if valid and positive
        - (None, None) if invalid input or non-positive values
        """
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            logger.info("User entered dimensions: %d rows, %d cols", rows, cols)
            if rows > 0 and cols > 0:
                return rows, cols
            else:
                logger.warning("Non-positive dimensions provided: rows=%d, cols=%d", rows, cols)
                return None, None
        except ValueError:
            logger.error("Invalid dimensions entered.")
            return None, None
