#!/usr/bin/env python

import inspect
import pkgutil
import sys
from importlib import import_module
from pathlib import Path

import jsonschema
import jsonschema.exceptions

from jiav import exceptions


class BaseBackend(object):
    """
    jiav base backend object

    All backends should inherit from this object

    Attributes:
        name   - Backend name
        valid  - Whether backend is valid
        schema - json_schema to be used to verify that the supplied setp
                 is valid according to the backends's requirments
        step   - Instructions to perform according to backend
    """

    def __init__(self, name=str(), schema=dict({}), step=dict({}), result=tuple()):
        self.name = name
        self.valid = False
        self.schema = schema
        self.step = step
        self.result = result

    def validate_schema(self):
        """
        Validates that the verification step is obeying the required
        schema

        Returns True if backend schema is valid
        """
        try:
            jsonschema.validate(instance=self.step, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            raise exceptions.InvalidManifestException(e)
        return True

    def execute_backend(self):
        """
        Executes backend

        This function should be overridden by each individual backend

        Returns False if this method is invoked directly and not overriden
        by backend
        """
        print(
            "Unable to execute BaseBackend, please invoke from real backend",
            "or backend does not override 'execute_backend' method",
        )
        return False


def import_backends():
    """
    Imports all valid backends from jiav/api/backends directory

    All valid backends are inherited from BaseBackend object

    Returns:
        exposed_backends - List of valid backend objects based on inherited
        from BaseBackend object
    """
    # TODO(vkhitrin): Perform additional checks if imported backend is valid
    # Init variables
    backend_classes = list()
    exposed_backends = dict({})

    for (_, name, _) in pkgutil.iter_modules([str(Path(__file__).parent)]):
        # Import all modules in directory
        imported_module = import_module("." + name, package=__name__)
        # Iterate over imported modules
        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            # If class in module inherits from BaseBackend,
            # add to valid backends
            if (
                inspect.isclass(attribute)
                and issubclass(attribute, BaseBackend)
                and attribute != BaseBackend
            ):
                setattr(sys.modules[__name__], name, attribute)
                backend_classes.append(attribute)
        # Expose supported backends
        for backend_class in backend_classes:
            backend_instance = backend_class()
            backend_name = backend_instance.name
            exposed_backends[backend_name] = backend_class
    return exposed_backends
