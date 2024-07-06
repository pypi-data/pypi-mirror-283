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
