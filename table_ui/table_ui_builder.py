from utilities import LOGGER_NAME
import logging
import sys

logger = logging.getLogger(LOGGER_NAME)

class TableUIBuilder:
    def __init__(self, controller):
        self.controller = controller
        logger.info(f"TableUIBuilder initialized with components.")
        self.setup_ui()

    def setup_ui(self):
        logger.info("Building UI components...")
        self.controller.nav_bar.build(self.controller)

        self.controller.lower_controls.build(self.controller.root, self.controller.lower_commands)

        self.controller.canvas_table.build(self.controller)
        self.bind_shortcuts()
        self.bind_table_scrolling()
        self.controller.canvas_table.highlight_active_cell()

    def bind_shortcuts(self):
        self.controller.root.bind('<Control-z>', lambda event: self.controller.undo())
        self.controller.root.bind('<Control-y>', lambda event: self.controller.redo())
        self.controller.root.bind("<Tab>",       lambda event: self.controller.handle_tab())
        self.controller.root.bind("<Print>",     lambda event: self.controller.take_screenshot_and_ocr())

    def bind_table_scrolling(self):
        """Bind mouse wheel scrolling to the table canvas."""
        canvas = self.controller.canvas_table.canvas

        if sys.platform == "darwin":
            # macOS: event.delta is usually ±1 per scroll
            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * e.delta, "units"))
            canvas.bind_all("<Shift-MouseWheel>", lambda e: canvas.xview_scroll(-1 * e.delta, "units"))
        else:
            # Windows: event.delta is usually ±120 per scroll
            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * int(e.delta / 120), "units"))
            canvas.bind_all("<Shift-MouseWheel>", lambda e: canvas.xview_scroll(-1 * int(e.delta / 120), "units"))
            # Linux: uses Button-4 and Button-5 for scrolling
            canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
            canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))