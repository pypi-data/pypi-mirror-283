#!/usr/bin/env python

schema = {
    "type": "object",
    "required": ["name", "backend"],
    "properties": {"name": {"type": "string"}, "backend": {"type": "string"}},
}
