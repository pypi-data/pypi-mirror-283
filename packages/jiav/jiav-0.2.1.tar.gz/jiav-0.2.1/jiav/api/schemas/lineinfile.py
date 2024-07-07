#!/usr/bin/env python

schema = {
    "type": "object",
    "required": ["path", "line"],
    "properties": {"path": {"type": "string"}, "line": {"type": "string"}},
    "additionalProperties": False,
}
