#!/usr/bin/env python3
"""Regex-ing"""
import re
from typing import List
import logging

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:  # nopep8
    """returns the log message obfuscated"""
    for val in fields:
        pattern = fr"{val}=.*?(?={separator})"
        message = re.sub(pattern, f"{val}={redaction}", message)
    return message


def get_logger() -> logging.Logger:
    """takes no arguments and returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


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
        initial_msg = super().format(record)  # Retrieves the original formatted message  # nopep8
        filter_msg = filter_datum(self.FIELDS, self.REDACTION, initial_msg, self.SEPARATOR)  # nopep8
        return filter_msg
