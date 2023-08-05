#!/usr/bin/env python3
"""Regex-ing"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:  # nopep8
    """returns the log message obfuscated"""
    for val in fields:
        pattern = fr"{val}=.*?(?={separator})"
        message = re.sub(pattern, f"{val}={redaction}", message)
    return message
