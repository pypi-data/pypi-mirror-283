#!/usr/bin/env python

schema = {
    "type": "object",
    "required": ["path", "regex"],
    "properties": {"path": {"type": "string"}, "regex": {"type": "string"}},
    "additionalProperties": False,
}
