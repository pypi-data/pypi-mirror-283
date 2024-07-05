import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    """
    Configures the logging settings for the application.

    This function sets up a logger with the following features:
    - Logs messages at the DEBUG level and above.
    - Uses a rotating file handler to manage log file sizes and backups.
    - Formats log messages with a specific format.
    - Ensures that log messages are also output to the console for real-time monitoring.

    Logging Details:
    - Log file path: 'logs/app.log'
    - Maximum log file size: 5 MB
    - Number of backup log files to keep: 3
    - Log message format: '%(asctime)s - %(levelname)s - %(filename)s - %(message)s'

    The rotating file handler helps in managing disk space by rotating the log file 
    once it reaches a specified size, and keeping a defined number of backup files.

    The console handler ensures that log messages are visible in the console in real-time,
    which is useful for debugging during development and monitoring in production.

    This setup prevents multiple handlers from being added if the function is called 
    more than once.
    """
    
    # Define log directory and file
    log_directory = "logs"
    log_file = os.path.join(log_directory, "app.log")

    # Ensure the log directory exists
    try:
        os.makedirs(log_directory, exist_ok=True)
    except OSError as e:
        print(f"Error creating log directory {log_directory}: {e}")
        return
    
    # Get the root logger instance
    logger = logging.getLogger()
    
    # Check if the logger already has handlers to prevent adding duplicate handlers
    if not logger.hasHandlers():
        try:
            # Set the logging level to DEBUG to capture all levels of log messages
            logger.setLevel(logging.DEBUG)

            # Create a rotating file handler to manage log files
            file_handler = RotatingFileHandler(
                log_file,                # Path to the log file
                maxBytes=5 * 1024 * 1024,      # Maximum file size: 5 MB
                backupCount=3                  # Number of backup files to keep
            )
            
            # Set the file handler's logging level to DEBUG
            file_handler.setLevel(logging.DEBUG)  # Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

            # Create a formatter to define the log message format
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(filename)s - %(message)s"  # Log message format
            )
            
            # Assign the formatter to the file handler
            file_handler.setFormatter(formatter)

            # Add the file handler to the logger
            logger.addHandler(file_handler)

            # Create a console handler to output log messages to the console
            console_handler = logging.StreamHandler()
            
            # Set the console handler's logging level to DEBUG
            console_handler.setLevel(logging.DEBUG)
            
            # Assign the formatter to the console handler
            console_handler.setFormatter(formatter)
            
            # Add the console handler to the logger
            logger.addHandler(console_handler)
        except Exception as e:
            print(f"Error setting up logging: {e}")

# Call setup_logging to configure logging when the module is imported
setup_logging()
