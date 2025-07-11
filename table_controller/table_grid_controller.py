from utilities import BG_COLOR, LOGGER_NAME
from table_ui import TableUIBuilder
from .table_interaction_coordinator import TableInteractionCoordinator

import logging

logger = logging.getLogger(LOGGER_NAME)

# === TableGridController: Wires together all table UI components and behaviors ===
class TableGridController:
    def __init__(self, window_manager, state, command_manager, nav, exporter, nav_bar, resize_controls, canvas_table):
        """
        Initialize the table controller with all required components.

        Parameters:
        - root: parent Tkinter window
        - state: GridStateManager (holds grid content and state)
        - nav: NavigationController (handles direction logic)
        - exporter: IExporter (e.g. CSVExporter)
        - nav_bar: NavigationBar (direction buttons)
        - resize_controls: ResizeControls (row/col adjustment)
        - canvas_table: TableCanvas (grid rendering)
        """
        self.window_manager = window_manager
        self.state = state
        self.command_manager = command_manager
        self.nav = nav
        self.exporter = exporter
        self.canvas_table = canvas_table
        self.nav_bar = nav_bar
        self.resize_controls = resize_controls

        self.callbacks = {
            "select_cell": self.select_cell,
            "start_edit": self.start_edit,
            "finish_edit": self.finish_edit,
        }

        self.navigation_items = {
            "nav_mode": self.set_nav_mode,
            "undo": self.undo,
            "redo": self.redo,
            "export": self.export,
            "screenshot_ocr": self.take_screenshot_and_ocr
        }

        self.root = window_manager.root

        self.handler = TableInteractionCoordinator(self)
        self.ui_builder = TableUIBuilder(self)

        logger.info("Initializing TableGridController UI components.")        

    def select_cell(self, row, col): 
        self.handler.nav_handler.select_cell(row, col)

    def apply_size_from_input(self):
        self.handler.resize_handler.apply_size_from_input()

    def undo(self):
        self.handler.history_handler.undo()

    def redo(self):
        self.handler.history_handler.redo()

    def insert_word(self, word):
        self.handler.word_inserter_handler.insert_word(word)

    def handle_tab(self):
        return self.handler.nav_handler.handle_tab()
    
    def select_cell(self, row,col):
        self.handler.nav_handler.select_cell(row, col)

    def set_nav_mode(self, mode):
        self.handler.nav_handler.set_nav_mode(mode)
    
    def start_edit(self, row, col):
        self.handler.cell_editor_handler.start_edit(row, col)
    
    def finish_edit(self, row, col):
        self.handler.cell_editor_handler.finish_edit(row, col)
    
    def export(self): 
        return self.exporter.export(self.state.grid_data)
    
    def take_screenshot_and_ocr(self):
        self.handler.screenshot_ocr_handler.start_ocr_processing()