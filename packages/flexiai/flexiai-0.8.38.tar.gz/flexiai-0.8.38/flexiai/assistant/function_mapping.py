import importlib.util
import os
import logging

logger = logging.getLogger(__name__)

def get_function_mappings():
    """
    Get the function mappings for personal and assistant functions, including both internal and user-defined functions.

    Returns:
        tuple: A tuple containing the personal function mappings and assistant function mappings.
    """
    # Internal function mappings
    personal_function_mapping = {}
    assistant_function_mapping = {}

    return personal_function_mapping, assistant_function_mapping

def register_user_functions(personal_function_mapping, assistant_function_mapping, user_module_path):
    """
    Register user-defined functions by merging them with existing function mappings.

    Args:
        personal_function_mapping (dict): The personal function mappings to be updated.
        assistant_function_mapping (dict): The assistant function mappings to be updated.
        user_module_path (str): Path to the user's module to load user-defined functions.

    Returns:
        tuple: A tuple containing the updated personal function mappings and assistant function mappings.
    """
    try:
        if os.path.isfile(user_module_path):
            module_name = os.path.basename(user_module_path).replace('.py', '')
            spec = importlib.util.spec_from_file_location(module_name, user_module_path)
            user_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(user_module)

            if hasattr(user_module, 'register_user_tasks'):
                user_personal_functions, user_assistant_functions = user_module.register_user_tasks()
                personal_function_mapping.update(user_personal_functions)
                assistant_function_mapping.update(user_assistant_functions)
                logger.info(f"Successfully registered user functions from {user_module_path}")
            else:
                raise AttributeError(f"The module at {user_module_path} does not have a 'register_user_tasks' function.")
        else:
            raise FileNotFoundError(f"The specified user module path {user_module_path} does not exist.")
    except Exception as e:
        logger.error(f"Failed to register user functions from {user_module_path}: {e}", exc_info=True)
        raise

    return personal_function_mapping, assistant_function_mapping
