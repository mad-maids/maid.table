def check_module(dictionary):
    """
    Checks if the module names are correct. This is done by checking against a
    ready list of modules that exist for undergrad.
    Returns True if the module names exist in the ready list.
    Otherwise returns the modules that are not listed in the 'modules' array.
    """
    modules = {
        "International Sales Law",
        "Negotiations and Influence",
        "Global Business Environment",
        "Public Law",
        "Introduction to Statistics and Data Science",
        "Financial Accounting",
        "International Economic Law",
        "Management Accounting",
        "Public International Law",
        "Digital Marketing",
        "Dissertation in Law",
        "Quality and Operations Management",
        "Introduction to Cryptocurrencies",
        "Marketing Management",
        "Financial Reporting",
        "Marketing Analytics",
        "I, Citizen",
        "Money and Banking",
        "Mathematics for Economists",
        "Corporate Governance for Finance",
        "Legal Skills",
        "Strategic Talent Management",
        "Machine Learning and Data Analytics",
        "Investment and Risk Management",
        "Company Law",
        "Fixed Income Securities",
        "Fashion and Lifestyle Marketing",
        "Cross Cultural Management",
        "Computer Science Fundamentals",
        "Introduction to Management and Organisational Behaviour",
        "Game Development",
        "Dissertation",
        "Developing Digital Enterprise",
        "Labour Economics",
        "Contemporary Issues in Global Economics",
        "Legal Profession and Legal Service",
        "Quantitative Methods",
        "Network Operations",
        "Brand Journalism and Content Strategy",
        "Strategy in a Complex World",
        "Distributed Systems and Cloud Computing",
        "International Investment Law",
        "Design Thinking for Learning",
        "Object Oriented Programming",
        "Consumer Behaviour",
        "Banking Theory and Practice",
        "Intermediate Microeconomics",
        "Financial Econometrics and Modelling",
        "Developing Professional Identity",
        "Strategic Management Accounting and Performance Me",
        "New Venture Creation",
        "Web Technology",
        "Introduction to Political Economy",
        "Applied Corporate Finance",
        "Development Economics",
        "Academic English",
        "Contract Law",
        "Mobile Application Development",
        "Business Information Systems Project",
        "Database Systems Development",
        "Project Management",
        "Fundametals of Programming",
        "Exploring Economics",
    }

    days = list(dictionary.values())

    # didnt want to write a lot of nested for loops, so here it goes
    module_names = {lesson["name"] for day in days if day for lesson in day}
    # this is roughly equivalent to:

    # module_names = set()
    # for day in days:
        # if day:
            # for lesson in day:
                # module_names.add(lesson["name"])

    if module_names.issubset(modules):
        return True
    else:
        # get the modules that are in module_names but not in modules
        difference = module_names - modules
        return difference

