# assistant/__init__.py
from flexiai.assistant.task_manager import TaskManager
from flexiai.assistant.function_mapping import get_function_mappings, register_user_functions

# Initialize TaskManager
task_manager = TaskManager()

# Get core function mappings
personal_function_mapping, assistant_function_mapping = get_function_mappings()

# Register user functions
personal_function_mapping, assistant_function_mapping = register_user_functions(personal_function_mapping, assistant_function_mapping)

__all__ = [
    'TaskManager',
    'personal_function_mapping',
    'assistant_function_mapping',
    'get_function_mappings',
]
