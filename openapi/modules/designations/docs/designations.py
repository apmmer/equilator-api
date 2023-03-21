"""
In this module are located text-maps (docs) for current package units.
It is convenient to store the types and descriptions of model fields
in a separate file to keep "DRYing".
The variables found here can also be used to create custom swagger
documentation.
"""

from pydantic import PositiveInt
from typing import Any, Dict

designation_scheme_docs: Dict[str, Dict[str, Any]] = {
    'id': {
        "type": "string",
        "title": "ID",
        "description": "ID-Hash of validated and sorted resulting chart.",
        "example": "c5f450a0f59240ddb5396c38bb3d852",
    },
    'range_definition': {
        "type": "string",
        "title": "Range definition",
        "description": "Definition of a range using a short string notation.",
        "example": "55-44,88,85s+,AKo",
    },
    'range_length': {
        "type": PositiveInt,
        "title": "Range definition",
        "description": "Definition of a range using a short string notation.",
        "example": 5,
    }
}
