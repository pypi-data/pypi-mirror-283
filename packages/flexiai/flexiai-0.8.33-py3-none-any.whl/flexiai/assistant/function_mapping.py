# assistant/function_mapping.py
from flexiai.user_flexiai_rag.user_function_mapping import register_user_tasks

def get_function_mappings(task_manager):
    """
    Get the function mappings for personal and assistant functions, including both internal and user-defined functions.

    Args:
        task_manager (TaskManager): The task manager instance containing internal tasks.

    Returns:
        tuple: A tuple containing the personal function mappings and assistant function mappings.
    """
    # FlexiAI's internal function mappings
    personal_function_mapping = {
        # Internal personal assistant functions here
    }

    assistant_function_mapping = {
        # Internal calling assistants here
    }

    # Register user-defined tasks
    user_personal_functions, user_assistant_functions = register_user_tasks()
    
    # Merge the user-defined functions with the internal ones
    personal_function_mapping.update(user_personal_functions)
    assistant_function_mapping.update(user_assistant_functions)

    return personal_function_mapping, assistant_function_mapping
