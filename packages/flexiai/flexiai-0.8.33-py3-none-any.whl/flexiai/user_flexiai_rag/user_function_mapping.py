# user_flexiai_rag/user_function_mapping.py
from flexiai.user_flexiai_rag.user_task_manager import UserTaskManager


def register_user_tasks():
    """
    Register user-defined tasks with the FlexiAI framework.

    Returns:
        tuple: A tuple containing the personal function mappings and assistant
        function mappings.
    """
    # Initialize UserTaskManager to access user-defined tasks
    task_manager = UserTaskManager()

    personal_function_mapping = {
        'search_youtube': task_manager.search_youtube,
        'search_products': task_manager.search_products,
        # Add other personal functions here
        # 'my_custom_task': task_manager.my_custom_task
    }

    assistant_function_mapping = {
        # Add other functions that call assistants here -> the functions must end with "_assistant"
        # 'call_example_assistant': task_manager.call_example_assistant,
    }

    return personal_function_mapping, assistant_function_mapping
