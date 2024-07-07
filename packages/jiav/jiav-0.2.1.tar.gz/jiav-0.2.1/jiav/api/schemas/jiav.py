#!/usr/bin/env python

schema = {
    "type": "object",
    "required": ["jiav"],
    "properties": {
        "jiav": {
            "type": "object",
            "required": ["verified_status", "verification_steps"],
            "properties": {
                "verification_steps": {"type": "array"},
                "verified_status": {"type": "string"},
            },
        }
    },
}
