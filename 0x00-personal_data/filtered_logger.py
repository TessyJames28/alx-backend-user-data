#!/usr/bin/env python3
"""Regex-ing"""
import re


def filter_datum(fields, redaction, message, separator) -> str:
    """returns the log message obfuscated"""
    for val in fields:
        message = re.sub(r"{}=.*?;".format(val), "{}={};".format(val, redaction), message)  # nopep8
    return message
