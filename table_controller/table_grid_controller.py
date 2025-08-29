from utilities import BG_COLOR, LOGGER_NAME
from table_ui import TableUIBuilder
from .table_interaction_coordinator import TableInteractionCoordinator

import logging

logger = logging.getLogger(LOGGER_NAME)

# === TableGridController: Wires together all table UI components and behaviors ===
class TableGridController:
    def __init__(self, window_manager, state, command_manager, nav, exporter, nav_bar, lower_controls, canvas_table):
        """
        Initialize the table controller with all required components.

        Parameters:
        - root: parent Tkinter window
        - state: GridStateManager (holds grid content and state)
        - nav: NavigationController (handles direction logic)
        - exporter: IExporter (e.g. CSVExporter)
        - nav_bar: NavigationBar (direction buttons)
        - lower_controls: LowerControls (row/col adjustment)
        - canvas_table: TableCanvas (grid rendering)
        """
        self.window_manager = window_manager
        self.state = state
        self.command_manager = command_manager
        self.nav = nav
        self.exporter = exporter
        self.canvas_table = canvas_table
        self.nav_bar = nav_bar
        self.lower_controls = lower_controls

        self.callbacks = {
            "select_cell": self.select_cell,
            "enter_edit_mode": self.enter_edit_mode,
            "exit_edit_mode": self.exit_edit_mode,
            "delete_cell_content": self.delete_cell_content,
            "start_edit": self.start_edit,
            "finish_edit": self.finish_edit,
        }

        self.lower_commands = {
            "clear_all_data": self.clear_all_data,
            "apply_size": self.apply_size_from_input,
            "insert_row": self.insert_row,
            "insert_col": self.insert_col
        }

        self.navigation_items = {
            "nav_mode": self.set_nav_mode,
            "undo": self.undo,
            "redo": self.redo,
            "export": self.export,
            "screenshot_ocr": self.take_screenshot_and_ocr,
            "clipboard_ocr": self.handle_clipboard_ocr
        }

        self.root = window_manager.root

        self.handler = TableInteractionCoordinator(self)
        self.ui_builder = TableUIBuilder(self)

        logger.info("Initializing TableGridController UI components.")        
       
    def enter_edit_mode(self, row, col):
        self.handler.mode_manager_handler.enter_edit_mode(row, col)
        
    def exit_edit_mode(self):
        self.handler.mode_manager_handler.exit_edit_mode()
        
    def delete_cell_content(self, row, col):
        self.handler.delete_cell_handler.delete_cell_content(row, col)

    def apply_size_from_input(self):
        self.handler.resize_handler.apply_size_from_input()

    def clear_all_data(self):
        self.handler.clear_handler.clear_with_confirmation()

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

    def handle_clipboard_ocr(self):
        self.handler.clipboard_ocr_handler.run_ocr_from_clipboard()

    def insert_row(self):
        self.handler.insert_row_handler.insert_row_before_current()

    def insert_col(self):
        self.handler.insert_col_handler.insert_col_before_current()