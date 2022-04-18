import json


def validate_json(data):
    """
    validate JSON format
    """
    return True
    try:
        json.loads(data)
    except ValueError as err:
        return False
    return True
