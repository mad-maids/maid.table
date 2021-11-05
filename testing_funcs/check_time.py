def check_time(dictionary):
    """
    Checks if the start time of the lesson is between 0 and 24.
    Returns true if they all are. Otherwise returns the start time that isn't.
    """
    days = list(dictionary.values())

    # didnt want to write a lot of nested for loops, so here it goes
    start_times = {lesson["start"] for day in days if day for lesson in day}
    # this is roughly equivalent to:

    # time_entries = set()
    # for day in days:
        # if day:
            # for lesson in day:
                # time_entries.add(lesson["start"])

    for start_time in start_times:
        if not (start_time >= 0 and start_time < 24):
            return start_time

    return True

