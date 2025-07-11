from .helper_funcs import resource_path

import logging
import os
import sys

LOGGER_NAME = resource_path("ocr_table_app")
LOGGING_PATH = resource_path("logs\\ocr_table_app.log")

def setup_logger():
    """
    Configures the logger for the OCR Table application.
    Sets up both file and console logging with appropriate formatting.
    Handles Unicode safely on Windows terminals.
    """
    # Ensure the logging directory exists
    os.makedirs(os.path.dirname(LOGGING_PATH), exist_ok=True)

    # Create a logger with the specified name
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        # === File handler (UTF-8 safe) ===
        file_handler = logging.FileHandler(LOGGING_PATH, encoding='utf-8')
        '''
        # === Console handler (safe for cp1251 terminals) ===
        class SafeStreamHandler(logging.StreamHandler):
            def emit(self, record):
                try:
                    msg = self.format(record)
                    stream = self.stream
                    stream.write(msg + self.terminator)
                    self.flush()
                except UnicodeEncodeError:
                    # Replace unprintable characters
                    record.msg = str(record.msg).encode('ascii', 'replace').decode()
                    super().emit(record)

        console_handler = SafeStreamHandler(stream=sys.stdout)

        '''
        # Format for all outputs
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        #console_handler.setFormatter(formatter)

        # Add both handlers
        logger.addHandler(file_handler)
        #logger.addHandler(console_handler)

    return logger
