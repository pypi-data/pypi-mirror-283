#!/usr/bin/env python

import os
import re
from collections import namedtuple

from jiav import logger
from jiav.api.backends import BaseBackend
from jiav.api.schemas.regexinfile import schema

MOCK_STEP = {"path": "/path/to/file", "regex": r"^.*$"}

# Subscribe to logger
jiav_logger = logger.subscribe_to_logger()


class RegexInFileBackend(BaseBackend):
    """
    RegexInFile backend object

    Checks if regex is in file

    Attributes:
        name   - Backend name
        schema - json_schema to be used to verify that the supplied step is
        valid according to the backends's requirements
        step   - Backend excution instructions
    """

    def __init__(self):
        self.name = "regexinfile"
        self.schema = schema
        self.step = MOCK_STEP
        super().__init__(self.name, self.schema, self.step)

    # Override method of BaseBackend
    def execute_backend(self):
        """
        Execute backend

        Returns a namedtuple describing the jiav manifest execution
        """
        # Parse required arugments
        file = self.step["path"]
        regex = self.step["regex"]
        # Create a namedtuple to hold the execution result output and errors
        result = namedtuple("result", ["successful", "output", "errors"])
        output = list()
        errors = list()
        successful = False
        compiled_regex = re.compile(rf"{regex}")
        if not os.path.exists(file):
            errors.append(f"File {file} does not exist")
        else:
            try:
                with open(file) as f:
                    file_content = f.read()
                    if not compiled_regex.search(file_content):
                        errors.append(f"Regex {regex} is not present in file {file}")
                        jiav_logger.error("Regex was not located in file")
                    else:
                        successful = True
                        output.append(f"Regex '{regex}' found in {file}")
                        jiav_logger.debug("Regex was located in file")
            except Exception as e:
                errors.append(f"OS exception: {str(e)}")
        self.result = result(successful, output, errors)
