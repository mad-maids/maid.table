def check_type(dictionary):
    """
    Checks if the lesson type is correct: lecture, online, seminar or workshop.
    If it is, returns True. Otherwise, returns the wrong lesson types.
    """
    all_types = {"lecture", "online", "seminar", "workshop"}

    days = list(dictionary.values())

    # didnt want to write a lot of nested for loops, so here it goes
    lesson_types = {lesson["type"] for day in days if day for lesson in day}
    # this is roughly equivalent to:

    # lesson_types = set()
    # for day in days:
        # if day:
            # for lesson in day:
                # lesson_types.add(lesson["type"])
 
    if lesson_types.issubset(all_types):
        return True
    else:
        # get the types that are not in all_types set
        difference = list(lesson_types - all_types)
        return difference

