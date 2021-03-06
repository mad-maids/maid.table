"""
This is the script to run all the tests.
Starts by running the Prettier formatter.
Checks all the .json files.
"""

import json
import os
import subprocess

from testing_funcs.enough_objects import enough_objects
from testing_funcs.check_module import check_module
from testing_funcs.verify_tutor import verify_tutor
from testing_funcs.check_type import check_type
from testing_funcs.check_time import check_time

# running prettier formatter prior to doing anything else
script = "yarn format:check --write"
command = script.split()
subprocess.run(command)

data_dir = os.path.join(os.getcwd(), "data")

file_paths = []
for subdir, dirs, files in os.walk(data_dir):
    for file in files:
        file_paths.append(os.path.join(subdir, file))


class TestClass:
    def test_quantity(self):
        for file_path in file_paths:
            with open(file_path) as file:
                data = json.load(file)
                assert enough_objects(data)

    def test_module_name(self):
        for file_path in file_paths:
            with open(file_path) as file:
                data = json.load(file)
                result = check_module(data)
                assert result == True, f"Module names {result} don't exist"

    def test_tutor_name(self):
        for file_path in file_paths:
            with open(file_path) as file:
                data = json.load(file)
                result = verify_tutor(data)
                assert result == True, f"Name is not upper case: {result}"

    def test_lesson_type(self):
        for file_path in file_paths:
            with open(file_path) as file:
                data = json.load(file)
                result = check_type(data)
                assert result == True, f"Lesson types {result} don't exist"

    def test_start_time(self):
        for file_path in file_paths:
            with open(file_path) as file:
                data = json.load(file)
                result = check_time(data)
                assert result == True, f"Time is out of bounds: {result}"

