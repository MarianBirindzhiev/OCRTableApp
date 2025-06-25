from utilities import LOGGER_NAME
import logging

logger = logging.getLogger(LOGGER_NAME)

class TableUIBuilder:
    def __init__(self, root, state, nav_bar, resize_controls, canvas_table, view):
        self.root = root
        self.state = state
        self.nav_bar = nav_bar
        self.resize_controls = resize_controls
        self.canvas_table = canvas_table
        self.view = view
        logger.info(f"TableUIBuilder initialized with {root} and state components.")

    def setup_ui(self):
        logger.info("Building UI components...")
        self.nav_bar.build(self.root, self.view.handler.set_nav_mode, self.view.handler.undo,
                           self.view.handler.redo, self.view.handler.export)
        
        self.resize_controls.build(self.root, self.view.handler.apply_size_from_input)

        self.canvas_table.build(self.root, self.state,
                                self.view.select_cell, self.view.start_edit,
                                self.view.finish_edit, self.view.handle_tab)
        self.bind_shortcuts()
        self.canvas_table.highlight_active_cell()

    def bind_shortcuts(self):
        self.root.bind('<Control-z>', lambda event: self.view.handler.undo())
        self.root.bind('<Control-y>', lambda event: self.view.handler.redo())
