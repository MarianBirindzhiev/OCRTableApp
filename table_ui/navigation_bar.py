from utilities import BG_COLOR, BUTTON_COLOR, BUTTON_HIGHLIGHT, BUTTON_ACTIVE_MODE, FONT, LOGGER_NAME

import logging
import tkinter as tk

logger = logging.getLogger(LOGGER_NAME)

class NavigationBar:
    def __init__(self):
        # Dictionary to hold references to mode buttons (→, ↓, ⟳)
        self.mode_buttons = {}
        logger.debug("NavigationBar initialized.")

    def build(self, controller):
        """
        Build the navigation bar UI and attach it to the root window.

        Parameters:
        - root: the parent tkinter widget
        - on_mode_change: callback when a navigation mode is selected
        - on_undo: callback for Undo action
        - on_redo: callback for Redo action
        - on_export: callback to export the grid data
        """
        logger.info("Building navigation bar UI.")
        self.nav_frame = tk.Frame(controller.root, bg=BG_COLOR)
        self.nav_frame.pack(pady=8)

        for mode in ("→", "↓", "⟳"):
            logger.debug(f"Creating mode button: {mode}")            
             # Create navigation mode buttons (→, ↓, ⟳)
            btn = tk.Button(
                self.nav_frame, text=mode,
                font=FONT, bg=BUTTON_COLOR,
                activebackground=BUTTON_HIGHLIGHT,
                relief="groove", padx=12, pady=6,
                command=lambda m=mode: controller.navigation_items["nav_mode"](m) # Capture current mode in lambda
            )
            btn.pack(side='left', padx=4)  # Arrange buttons horizontally
            self.mode_buttons[mode] = btn
        # Create action buttons (Undo, Redo, Export)
        for text, command in [
            ("Undo", controller.navigation_items["undo"]),
            ("Redo", controller.navigation_items["redo"]),
            ("Export", controller.navigation_items["export"]),
            ("Screenshot & OCR", controller.navigation_items["screenshot_ocr"])
        ]:
            logger.debug(f"Creating action button: {text}")            
            tk.Button(
                self.nav_frame, text=text, command=command,
                font=FONT, bg=BUTTON_COLOR,
                activebackground=BUTTON_HIGHLIGHT,
                relief="groove", padx=12, pady=6
            ).pack(side='left', padx=4)

        self.update_mode_buttons('→')
        logger.info("Navigation bar UI built successfully.")

    def update_mode_buttons(self, active_mode):
        """
        Highlight the active navigation mode button.

        Parameters:
        - active_mode: the currently selected mode (→, ↓, ⟳)
        """
        logger.info(f"Navigation mode changed to: {active_mode}")
        for mode, btn in self.mode_buttons.items():
            if mode == active_mode:
                btn.config(state="active", bg = BUTTON_ACTIVE_MODE)
            else:
                btn.config(state="normal", bg = BUTTON_COLOR)
