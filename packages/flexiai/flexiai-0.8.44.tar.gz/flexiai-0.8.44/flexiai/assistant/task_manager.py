# assistant/task_manager.py
import logging
from flexiai.config.logging_config import setup_logging

# Set up logging using your custom configuration
setup_logging(root_level=logging.INFO, file_level=logging.DEBUG, console_level=logging.ERROR)

class TaskManager:
    """
    TaskManager class handles tasks related to searching YouTube, searching products,
    and integrates user-defined tasks.
    """

    def __init__(self):
        """
        Initializes the TaskManager instance, setting up the logger and user-defined tasks.
        """
        self.logger = logging.getLogger(__name__)
        self.load_user_tasks()

    def load_user_tasks(self):
        """
        Dynamically load and integrate user-defined tasks.
        """
        from flexiai.assistant.function_mapping import register_user_functions, get_function_mappings
        
        self.personal_function_mapping, self.assistant_function_mapping = get_function_mappings()
        self.personal_function_mapping, self.assistant_function_mapping = register_user_functions(self.personal_function_mapping, self.assistant_function_mapping)
