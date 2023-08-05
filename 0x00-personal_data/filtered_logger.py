#!/usr/bin/env python3
"""Regex-ing"""
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:  # nopep8
    """returns the log message obfuscated"""
    for val in fields:
        pattern = fr"{val}=.*?(?={separator})"
        message = re.sub(pattern, f"{val}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.FIELDS = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        initial_msg = super().format(record)
        filter_msg = filter_datum(self.FIELDS, self.REDACTION, initial_msg, self.SEPARATOR)  # nopep8
        return filter_msg
