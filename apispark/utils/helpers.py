import logging
import traceback

def log_error(error_message: str, exception: Exception = None):
    """
    Logs error messages with traceback details if available.
    """
    logging.error(f"Error: {error_message}")
    if exception:
        logging.error(f"Exception: {exception}")
        traceback.print_exc()
