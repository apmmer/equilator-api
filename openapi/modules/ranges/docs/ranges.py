"""
In this module are located text-maps (docs) for current package units.
It is convenient to store the types and descriptions of model fields
in a separate file to keep "DRYing".
The variables found here can also be used to create custom swagger
documentation.
"""

from typing import Any, Dict

range_scheme_docs: Dict[str, Dict[str, Any]] = {
    'id': {
        "type": "integer",
        "title": "ID",
        "description": "Unique autoincremented ID in db.",
        "example": 1,
    },
    'hash': {
        "type": "string",
        "title": "Hash",
        "description": (
            "Hash of validated and sorted resulting range. "
            "It should be calculated automatically on backend side."
        ),
        "example": "c5f450a0f59240ddb5396c38bb3d852",
    },
    'name': {
        "type": "string",
        "title": "Name",
        "description": (
            "Associated unique situation"
            " where current range can be used."),
        "example": "My 4-Bet range from UTG-3",
    },
    'definition': {
        "type": "object",
        "title": "Range definition",
        "description": (
            "Definition of a range, a map, which "
            "includes hands names and weight."
        ),
        "example": {
            "AhAd": 1.0,
            "AhAc": 1.0,
            "AhAs": 1.0,
            "AdAc": 1.0,
            "AhKh": 0.5,
            "AdKd": 0.5,
            "AcKc": 0.5,
            "AsKs": 0.5,
            "KhKd": 0.9,
            "KcKs": 0.9,
        },
    }
}
