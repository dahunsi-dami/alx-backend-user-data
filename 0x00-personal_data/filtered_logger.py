#!/usr/bin/env python3
"""String obfuscation module that obfuscates data with regex."""

import re
import logging
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:  # noqa: E501
    """
    Uses regex to replace occurrences of certain field values.

    Args:
        fields: list of strings repping all field to obfuscate.
        redaction: string repping by what field will be obfuscated.
        message: a string representing the log line.
        separator: string repped by which char separates all fields-
        -in log line (message).

    Returns:
        the log message obfuscated.
    """
    pattern = f"({'|'.join(fields)})=[^({separator})]*"
    return re.sub(
        pattern,
        lambda match: f"{match.group().split('=')[0]}={redaction}",
        message
    )

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.message = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super().format(record)