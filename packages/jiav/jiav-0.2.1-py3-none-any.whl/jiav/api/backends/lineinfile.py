#!/usr/bin/env python

import os
from collections import namedtuple

from jiav import logger
from jiav.api.backends import BaseBackend
from jiav.api.schemas.lineinfile import schema

MOCK_STEP = {"path": "/path/to/file", "line": "line_in_file"}

# Subscribe to logger
jiav_logger = logger.subscribe_to_logger()


class LineInFileBackend(BaseBackend):
    """
    LineInFile backend object

    Checks if line is in file

    Attributes:
        name   - Backend name
        schema - json_schema to be used to verify that the supplied step is
        valid according to the backends's requirements
        step   - Backend excution instructions
    """

    def __init__(self):
        self.name = "lineinfile"
        self.schema = schema
        self.step = MOCK_STEP
        super().__init__(self.name, self.schema, self.step)

    # Overrdie method of BaseBackend
    def execute_backend(self):
        """
        Execute backend

        Returns a namedtuple describing the jiav manifest execution
        """
        # Parse required arugments
        file = self.step["path"]
        line = self.step["line"]
        # Create a namedtuple to hold the execution result output and errors
        result = namedtuple("result", ["successful", "output", "errors"])
        output = list()
        errors = list()
        successful = False
        jiav_logger.debug(f"File: {file}")
        jiav_logger.debug(f"Line: {line}")
        # Check if file exits
        if not os.path.exists(file):
            errors.append(f"File {file} does not exist")
        else:
            try:
                with open(file) as f:
                    file_content = f.read()
                    if line not in file_content:
                        errors.append(f"Line {line} is not present in file {file}")
                        jiav_logger.error("Line was not located in file")
                    else:
                        successful = True
                        output.append(f"Line '{line}' found in {file}")
                        jiav_logger.debug("Line was located in file")
            except Exception as e:
                errors.append(f"OS exception: {str(e)}")
        self.result = result(successful, output, errors)
