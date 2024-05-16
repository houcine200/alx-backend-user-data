#!/usr/bin/env python3
'''Handle Personal Data.'''
import re
from typing import List
def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """Filter sensitive data in a message.
    """
    import re

def filter_datum(fields, redaction, message, separator):
    for field in fields:
        message = re.sub(fr'\b{field}\b', redaction, message)
    return message
