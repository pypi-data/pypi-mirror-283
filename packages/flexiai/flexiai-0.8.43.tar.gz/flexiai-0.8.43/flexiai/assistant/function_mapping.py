# assistant/function_mapping.py
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

def register_user_functions(personal_function_mapping, assistant_function_mapping):
    """
    Register user-defined functions by merging them with existing function mappings.

    Args:
        personal_function_mapping (dict): The personal function mappings to be updated.
        assistant_function_mapping (dict): The assistant function mappings to be updated.

    Returns:
        tuple: A tuple containing the updated personal function mappings and assistant function mappings.
    """
    try:
        from user_flexiai_rag.user_function_mapping import register_user_tasks

        user_personal_functions, user_assistant_functions = register_user_tasks()
        personal_function_mapping.update(user_personal_functions)
        assistant_function_mapping.update(user_assistant_functions)
        logger.info("Successfully registered user functions from user_flexiai_rag/user_function_mapping.py")

    except ModuleNotFoundError:
        logger.warning("The module user_flexiai_rag.user_function_mapping does not exist.")
    except AttributeError:
        logger.error("The module user_flexiai_rag.user_function_mapping does not have a 'register_user_tasks' function.")
    except Exception as e:
        logger.error(f"Failed to register user functions: {e}", exc_info=True)
        raise

    return personal_function_mapping, assistant_function_mapping
