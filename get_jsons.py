"""
Scrapes the intranet timetable page. Gets all the lessons data for undergrad, 
saves it in .json format in the data folder. test
"""

import json
import logging
import random
import re
import time
from pathlib import Path

from environs import Env
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options


logging.basicConfig(level=logging.INFO, format="#%(levelname)-8s %(message)s")

env = Env()
env.read_env()

# Workflow is failing if the browser window is not maximized.
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# these are saved in the .env file
USER_ID = env.str("USER_ID")
PASSWORD = env.str("PASSWORD")

# create an instance of and launch chrome webdriver
browser = webdriver.Chrome(options=chrome_options)

# make a GET request to intranet timetable
browser.get("https://intranet.wiut.uz/TimeTableNew/GetLessons")

# filling in user id
userid_field = browser.find_element(
    By.XPATH, "/html/body/div[2]/div[2]/div[2]/section/form/fieldset/div[1]/div/input"
)
userid_field.click()
userid_field.send_keys(USER_ID)

# filling in password
password_field = browser.find_element(
    By.XPATH, "/html/body/div[2]/div[2]/div[2]/section/form/fieldset/div[2]/div/input"
)
password_field.click()
password_field.send_keys(PASSWORD)
password_field.send_keys(Keys.ENTER)

# group selection dropdown menu
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)

try:
    select = Select(
        WebDriverWait(browser, 15, ignored_exceptions=ignored_exceptions).until(
            expected_conditions.presence_of_element_located((By.ID, "ddlclass"))
        )
    )
except TimeoutException:
    browser.quit()
    raise SystemExit("No groups were found. No timetable available.")

# this is just a list of all group names
all_groups = [option.text for option in select.options]

# the first 2 elements in all_groups array are an empty blank and '1 time'
for group in all_groups[2:]:
    # skip lyceum groups
    if re.search(r"UzG|RuG", group, re.IGNORECASE):
        continue

    # undergrad ends here i guess (also their time entries are a bit different)
    if group == "7MScBIA1":
        break

    logging.info(f"Getting data for {group}")

    # element may change or may not be avaiable in the DOM, this handles these
    # exceptions by waiting
    select = Select(
        WebDriverWait(browser, 15, ignored_exceptions=ignored_exceptions).until(
            expected_conditions.presence_of_element_located((By.ID, "ddlclass"))
        )
    )
    select.select_by_visible_text(group)

    # divs -> all boxes that contain info on classes
    # there are 66 of them, 11 per day for 6 days (Monday-Saturday)
    divs = browser.find_elements(
        By.CSS_SELECTOR,
        "div.innerbox[style='overflow-y: auto; overflow-x: hidden;  "
        "font-size:medium']",
    )

    days = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7":[]}

    for index, div in enumerate(divs):
        # this represents a non-empty div (a box that has class info)
        if div.text:
            # this whole script works thanks to the fact that all class details
            # are formatted the same for undergrad
            class_details = div.text.split("\n")

            # the following blocks deal with obtaining the info from the string
            tutor = class_details[-1]
            name = class_details[-2]

            if "online" in name.lower():
                name = name.split(" / ")[-1]
                class_type = "online"
            elif "lec" in name:
                class_type = "lecture"
            elif name.split("_")[1][0] == "w":
                class_type = "workshop"
            else:
                class_type = "seminar"

            location = class_details[-3]

            if "(" in location:
                kill_brackets_re = r"\(\d+\)"
                brackets_match = re.search(kill_brackets_re, location)
                
                if brackets_match:
                    br_range = brackets_match.span()
                    location = location[:br_range[0]] + location[br_range[1]:]
                    # to get rid of duplicate whitespace
                    location = " ".join(location.split())

                else:
                    location = location.split("(")[0].strip()

            name = name.split("_")[0]

            # i hate to make this code even more loaded, but one module name is
            # incomplete on intranet timetable page
            if name.endswith("Beha"):
                name += "viour"

            day = str((index // 11) + 1)
            class_time = 9.0 + (index % 11)

            ready_details = {
                "name": name,
                "tutor": tutor,
                "type": class_type,
                "start": class_time,
                "length": 1.0,
                "location": location,
            }

            try:
                last_class = days[day][-1]
            except IndexError:
                last_class = {}

            # conditions for the if check (it got messy without them)
            same_name = last_class.get("name") == name
            same_type = last_class.get("type") == class_type

            # sometimes the second hour of the lecture has the 'w' mark instead
            # of the 'lec' mark
            edge_case = last_class.get("type") == "lecture" and class_type == "workshop"

            if last_class and same_name and (same_type or edge_case):
                last_class["length"] += 1.0
            else:
                days[day].append(ready_details)

    group = group.upper()

    # obtaining the course name (e.g. 5BIS, 6ECwF, etc.)
    course_regex = r"[3-6]\D+"
    course = re.search(course_regex, group)
    assert course is not None
    course = course.group()

    # creating the relevant dir if it doesn't exit
    Path(f"./data/{course}").mkdir(parents=True, exist_ok=True)

    with open(f"./data/{course}/{group}.json", "w") as output:
        # indent is indicated to apply pretty formatting
        json.dump(days, output, indent=4)

    # to be on the safe side and not send a ton of requests in a short time
    # random is used so that it seems like a human is actually doing this
    time.sleep(random.uniform(2, 3))

browser.quit()
