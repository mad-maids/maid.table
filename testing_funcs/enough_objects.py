def enough_objects(dictionary):
    """
    Checks whether the json (converted to a dict) has enough objects (Monday-Sunday)
    Returns True if it does, False otherwise.
    """
    keys = list(dictionary.keys())
    # still have no idea why there's 8 keys instead of 7
    reference = ["0", "1", "2", "3", "4", "5", "6", "7"]

    return keys == reference

