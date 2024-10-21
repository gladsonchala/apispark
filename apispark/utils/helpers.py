import logging
import traceback

def log_error(error_message: str, exception: Exception = None):
    logging.error(f"Error: {error_message}")
    if exception:
        logging.error(f"Exception: {exception}")
        traceback.print_exc()
