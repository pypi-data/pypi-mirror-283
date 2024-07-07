# assistant/__init__.py
from flexiai.config.config import config  # Import the config to use the loaded environment variables
from flexiai.assistant.task_manager import TaskManager
from flexiai.assistant.function_mapping import get_function_mappings, register_user_functions

# Get the path to the user-defined functions and task manager from the environment variables
user_task_manager_path = config.USER_TASK_MANAGER_PATH

# Initialize TaskManager
task_manager = TaskManager(user_task_manager_path)

# Get core function mappings
personal_function_mapping, assistant_function_mapping = get_function_mappings()

# Register user functions
personal_function_mapping, assistant_function_mapping = register_user_functions(personal_function_mapping, assistant_function_mapping, user_task_manager_path)

__all__ = [
    'TaskManager',
    'personal_function_mapping',
    'assistant_function_mapping',
    'get_function_mappings',
]
