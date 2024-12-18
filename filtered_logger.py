#!/usr/bin/env python3
"""String obfuscation module that obfuscates data with regex."""

import re


def filter_datum(fields, redaction, message, separator):
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
