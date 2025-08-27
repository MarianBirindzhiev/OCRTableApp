from utilities import LOGGER_NAME
import logging

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
        self.controller.canvas_table.highlight_active_cell()

    def bind_shortcuts(self):
        self.controller.root.bind('<Control-z>', lambda event: self.controller.undo())
        self.controller.root.bind('<Control-y>', lambda event: self.controller.redo())
        self.controller.root.bind("<Tab>",       lambda event: self.controller.handle_tab())
        self.controller.root.bind("<Print>",  lambda event: self.controller.take_screenshot_and_ocr())
