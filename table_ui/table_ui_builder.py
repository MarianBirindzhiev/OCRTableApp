from utilities import LOGGER_NAME
import logging

logger = logging.getLogger(LOGGER_NAME)

class TableUIBuilder:
    def __init__(self, view):
        self.view = view
        logger.info(f"TableUIBuilder initialized with components.")
        self.setup_ui()

    def setup_ui(self):
        logger.info("Building UI components...")
        self.view.nav_bar.build(self.view.root, self.view.set_nav_mode, self.view.undo,
                           self.view.redo, self.view.export)

        self.view.resize_controls.build(self.view.root, self.view.apply_size_from_input)

        self.view.canvas_table.build(self.view)
        self.bind_shortcuts()
        self.view.canvas_table.highlight_active_cell()

    def bind_shortcuts(self):
        self.view.root.bind('<Control-z>', lambda event: self.view.undo())
        self.view.root.bind('<Control-y>', lambda event: self.view.redo())
        self.view.root.bind("<Tab>",       lambda event: self.view.handle_tab())
