# core/utils/helpers.py
import json
import logging


def show_json(obj):
    """
    Print a JSON object using a custom model_dump_json method.
    """
    print(json.dumps(json.loads(obj.model_dump_json()), indent=4))


def pretty_print(messages):
    """
    Pretty print a list of message objects.
    """
    print("=" * 100)
    for msg in messages:
        role = msg['role']
        content_value = msg['content']

        role_name = "User" if role == "user" else "Assistant"
        print(f"{role_name}: {content_value}")
    print("=" * 100)
    print()


def print_run_details(run):
    """
    Print the details of a run object.
    """
    try:
        if hasattr(run, 'dict'):
            print(json.dumps(run.dict(), indent=4))
        else:
            print(json.dumps(run, default=lambda o: o.__dict__, indent=4))
    except TypeError as e:
        logging.error(f"Error serializing object: {e}")
        print(run)
        

def print_messages_as_json(messages):
    """
    Print messages returned by the retrieve_message_object function in JSON format.

    Args:
        messages (list): List of message objects returned by retrieve_message_object.
    """
    def content_block_to_dict(content_block):
        """
        Convert a TextContentBlock object to a dictionary.
        """
        content_block_dict = content_block.__dict__.copy()
        if hasattr(content_block, 'text') and isinstance(content_block.text, object):
            content_block_dict['text'] = content_block.text.__dict__
        return content_block_dict

    def message_to_dict(message):
        """
        Convert a message object to a dictionary, including nested TextContentBlock objects.
        """
        message_dict = message.__dict__.copy()
        if 'content' in message_dict:
            message_dict['content'] = [content_block_to_dict(content) for content in message_dict['content']]
        return message_dict

    # Convert each message object to a dictionary
    messages_dict = [message_to_dict(message) for message in messages]
    # Print the messages in JSON format
    print(json.dumps(messages_dict, indent=4))

