#!/usr/bin/env python3
"""Write a function called filter_datum that returns the log """
import logging
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, seperator: str
        ) -> str:
    """Returns the log message obfuscated"""
    for field in fields:
        message = re.sub(f"{field}=.+?{seperator}",
                         f"{field}={redaction}{seperator}", message)
    return message
