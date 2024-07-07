#!/usr/bin/env python

import importlib.metadata

import jiav.api.backends

__VERSION__ = importlib.metadata.version("jiav")
EXPOSED_BACKENDS = jiav.api.backends.import_backends()
