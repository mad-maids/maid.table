"""
Scrapes the intranet timetable page. Gets all the lessons data for undergrad, 
saves it in .json format in the data folder. test
"""

import json
import logging
from pathlib import Path
import random
import re
import shutil
import time

from environs import Env
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select, WebDriverWait


env = Env()
env.read_env()

# -------------------- REGEX --------------------
KILL_BRACKETS_RE = re.compile(r"\s?\(\s?\d+\s?\)")
GROUP_RE = re.compile(
    r"\d(CIFS|BABM|BIS|CL|ECwF|Fin|BMFin|BMMar)\d+|MScBIA|(MAIBM 1)",
    re.IGNORECASE,
)
COURSE_RE = re.compile(r"[3-6]\D+|MSCBIA")

# -------------------- OTHER CONSTANTS --------------------
USER_ID = env.str("USER_ID")
PASSWORD = env.str("PASSWORD")

# -------------------- FUNCTIONS --------------------
def sign_in(sel_browser, user_id, password) -> None:
    """Sign in to the intranet site using user_id and password."""
    userid_field = sel_browser.find_element(
        By.XPATH,
        "/html/body/div[2]/div[2]/div[2]/section/form/fieldset/div[1]/div/input",
    )
    userid_field.click()
    userid_field.send_keys(user_id)

    password_field = sel_browser.find_element(
        By.XPATH,
        "/html/body/div[2]/div[2]/div[2]/section/form/fieldset/div[2]/div/input",
    )
    password_field.click()
    password_field.send_keys(password)
    password_field.send_keys(Keys.ENTER)


def process_location(class_location: str, useless_part: re.Pattern) -> str:
    """Remove unnecessary part from the location string.

    This function's main purpose is to remove the stuff inside (and including)
    brackets from locations like: ATB212 (27) CL, IB303(26), ATB310(25 )B, etc

    >>> process_location("ATB212 (27) CL", KILL_BRACKETS_RE)
    "ATB212 CL"

    Parameters
    ----------
    class_location : str
        where the class is going to be held

    Returns
    -------
    str
        the location without the unnecessary part
    """

    match = re.search(useless_part, class_location)

    if match:
        start, end = match.span()
        class_location = class_location[:start] + class_location[end:]

    return class_location


def process_class_data(class_data: list, slot_index: int) -> dict:
    """Process class data (idk what else to write here).

    Parameters
    ----------
    class_data : list
        looks like: ['location', 'module name_sem_blah_blah', 'teacher name']
    slot_index : int
        the index position of the slot in the timetable (used to figure out
        class time)

    Returns
    -------
    dict
        a dictionary that contains all the processed data (ready to work with)
    """

    if len(class_data) == 2:
        # rn this happens with some 6CL students and theres no location
        class_data.insert(0, "void")

    location, tutor = class_data[0], class_data[2]
    class_name, class_type = class_data[1].split("_", maxsplit=1)
    class_time = 9.0 + (slot_index % 11)

    # i hate to make this code even more loaded, but one module name is
    # incomplete on intranet timetable page (4BABM)
    if class_name.endswith("Beha"):
        class_name += "viour"

    if "lec" in class_type:
        class_type = "lecture"
    elif "w" in class_type:
        class_type = "workshop"
    else:
        class_type = "seminar"

    location = process_location(location, KILL_BRACKETS_RE)

    processed_data = {
        "name": class_name,
        "tutor": tutor,
        "type": class_type,
        "start": class_time,
        "length": 1.0,
        "location": location,
    }

    return processed_data


# -------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="#%(levelname)-8s %(message)s")

# Workflow is failing if the browser window is not maximized.
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# create an instance of and launch chrome webdriver
browser = webdriver.Chrome(options=chrome_options)

# make a GET request to intranet timetable
browser.get("https://intranet.wiut.uz/TimeTableNew/GetLessons")

sign_in(browser, USER_ID, PASSWORD)

# group selection dropdown menu
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)

try:
    select = Select(
        WebDriverWait(
            browser, 15, ignored_exceptions=ignored_exceptions
        ).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "ddlclass")
            )
        )
    )
except TimeoutException:
    browser.quit()
    raise SystemExit("No groups were found. No timetable available.")

# delete old timetable data
shutil.rmtree("./data/", ignore_errors=True)

# this is just a list of all undergrad + MSCBIA group names
all_groups = [
    option.text
    for option in select.options
    if re.search(GROUP_RE, option.text)
]

for group in all_groups:
    if group == "MAIBM 1":
        continue

    logging.info(f"Getting data for {group}")

    # element may change or may not be avaiable in the DOM, this handles these
    # exceptions by waiting
    select = Select(
        WebDriverWait(
            browser, 15, ignored_exceptions=ignored_exceptions
        ).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "ddlclass")
            )
        )
    )
    select.select_by_visible_text(group)

    # slots -> all boxes that contain info on classes
    # there are 66 of them, 11 per day for 6 days (Monday-Saturday)
    slots = browser.find_elements(
        By.CSS_SELECTOR,
        "div.innerbox[style='overflow-y: auto; overflow-x: hidden;  "
        "font-size:medium']",
    )

    days = {str(n): [] for n in range(8)}

    for index, slot in enumerate(slots):
        # no class in this time slot
        if not slot.text:
            continue

        day = str((index // 11) + 1)

        # this whole script works thanks to the fact that all class details
        # are formatted more or less the same
        data = slot.text.splitlines()

        # removing the group names from this list so that it looks like:
        # ['some location', 'module name_sem_blah_blah', 'teacher name']
        data = [entry for entry in data if not re.search(GROUP_RE, entry)]

        # splitting the data list into sublists because sometimes theres more
        # than 1 class scheduled in 1 time slot
        # [., ., ., ., ., .] -> [[...], [...]]
        classes_data = [data[i : i + 3] for i in range(0, len(data), 3)]

        for data in classes_data:
            processed_data = process_class_data(data, index)

            # if theres a collision -> 2 or more classes in one time slot:
            # we want to check the length of the last and prelast class
            if len(classes_data) > 1:
                end = -3
            else:
                end = -2

            for i in range(-1, end, -1):
                try:
                    past_class = days[day][i]
                except IndexError:
                    past_class = {}

                # conditions for the if check (it got messy without them)
                same_name = past_class.get("name") == processed_data["name"]
                same_type = past_class.get("type") == processed_data["type"]

                # Subair's lectures - 1hour lecture & 1hour workshop, but many
                # consider this 2-hour lecture, it will be classified like that
                edge_case = (
                    past_class.get("type") == "lecture"
                    and past_class.get("name") == processed_data["name"]
                    and processed_data["type"] == "workshop"
                    and past_class.get("length") == 1
                )

                if past_class and same_name and (same_type or edge_case):
                    past_class["length"] += 1.0
                    # if we break, the else block won't run
                    break
            else:
                days[day].append(processed_data)

    group = group.upper()
    course = re.search(COURSE_RE, group)
    assert course is not None
    course = course.group()

    # creating the relevant dir if it doesn't exit
    Path(f"./data/{course}").mkdir(parents=True, exist_ok=True)

    with open(f"./data/{course}/{group}.json", "w") as output:
        json.dump(days, output, indent=2)

    # to be on the safe side and not send a ton of requests in a short time
    # random is used so that it seems like a human is actually doing this
    time.sleep(random.uniform(2, 3))

browser.quit()
