def verify_tutor(dictionary):
    """
    Checks if the tutors' names start with an uppercase letter.
    Returns true if they all do. Otherwise returns the name that doesn't.
    """
    days = list(dictionary.values())

    # didnt want to write a lot of nested for loops, so here it goes
    tutor_names = {lesson["tutor"] for day in days if day for lesson in day}
    # this is roughly equivalent to:

    # tutor_names = set()
    # for day in days:
        # if day:
            # for lesson in day:
                # tutor_names.add(lesson["tutor"])

    for tutor in tutor_names:
        # couldnt use the simple .istitle() method here since some tutors have
        # weird middle names (e.g. AKM)
        names = tutor.split()
        upper_names = [name[0].isupper() for name in names]

        if not all(upper_names):
            return tutor

    return True

