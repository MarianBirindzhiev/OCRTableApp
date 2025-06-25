from utilities import BG_COLOR, LOGGER_NAME
from .table_ui_builder import TableUIBuilder
from .table_interaction_handler import TableInteractionHandler

import logging

logger = logging.getLogger(LOGGER_NAME)

# === TableGridView: Wires together all table UI components and behaviors ===
class TableGridView:
    def __init__(self, root, state, nav, word_inserter, exporter, nav_bar, resize_controls, canvas_table):
        """
        Initialize the table view with all required components.

        Parameters:
        - root: parent Tkinter window
        - state: GridStateManager (holds grid content and state)
        - nav: NavigationController (handles direction logic)
        - word_inserter: WordInserter (inserts OCR words into grid)
        - exporter: IExporter (e.g. CSVExporter)
        - nav_bar: NavigationBar (direction buttons)
        - resize_controls: ResizeControls (row/col adjustment)
        - canvas_table: TableCanvas (grid rendering)
        """
        self.root = root
        self.state = state
        self.nav = nav
        self.word_inserter = word_inserter
        self.exporter = exporter
        self.canvas_table = canvas_table
        self.nav_bar = nav_bar
        self.resize_controls = resize_controls

        self.ui_builder = TableUIBuilder(
            root, state, nav_bar, resize_controls, canvas_table, self
        )
        self.handler = TableInteractionHandler(
            state, nav, word_inserter, exporter, canvas_table, self
        )

        self.ui_builder.setup_ui()
        logger.info("Initializing TableGridView UI components.")        

    def select_cell(self, row, col): self.handler.select_cell(row, col)
    def start_edit(self, row, col): self.handler.start_edit(row, col)
    def finish_edit(self, row, col): self.handler.finish_edit(row, col)
    def handle_word_insert(self, word): self.handler.handle_word_insert(word)
    def handle_tab(self, event): return self.handler.handle_tab(event)