# assistant/task_manager.py
import logging
from flexiai.config.logging_config import setup_logging
from flexiai.user_flexiai_rag.user_task_manager import UserTaskManager

# Set up logging using your custom configuration
setup_logging()

class TaskManager(UserTaskManager):  # Inherit from UserTaskManager
    """
    TaskManager class handles tasks related to searching YouTube, searching products,
    and integrates user-defined tasks.
    """

    def __init__(self):
        """
        Initializes the TaskManager instance, setting up the logger and user-defined tasks.
        """
        super().__init__()  # Initialize UserTaskManager
        self.logger = logging.getLogger(__name__)

    # Add more internal task manager functions if needed
