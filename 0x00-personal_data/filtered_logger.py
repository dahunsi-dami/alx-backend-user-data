#!/usr/bin/env python3
"""String obfuscation module that obfuscates data with regex."""

import os
import re
import logging
import mysql.connector
from mysql.connector import connection
from typing import List, Tuple

PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


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
    """
    This is the redacting formatter class.

    Filters values in incoming log records w/ filter_datum,
    while values for fields in `fields` should be filtered.

    FORMAT mustn't be extrapolated manually, and
    format method should be < 5 lines long.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the RedactingFormatter.

        Args:
            fields: list of field names to be obfuscated in log record.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Applies the filter to obfuscate specced fields in log record.

        Args:
            record: log record w/ message to be formatted.

        Returns:
            str: formatted log message w/ obfuscated fields.
        """
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.getMessage(),
            self.SEPARATOR + ' '
        )
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger for user data.

    The logger:
    - Is named "user_data".
    - Logs up to INFO level.
    - Does not propagate to other loggers.
    - Has a StreamHandler with RedactingFormatter applied to it.

    Returns:
        logging.Logger: Configured logger instance for user data.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """
    Establishes and returns a secure connection to a MySQL database.

    The function retrieves database credentials from environment variables:
    - PERSONAL_DATA_DB_USERNAME: Database username (default: 'root').
    - PERSONAL_DATA_DB_PASSWORD: Database password (default: empty string).
    - PERSONAL_DATA_DB_HOST: Database host (default: 'localhost').
    - PERSONAL_DATA_DB_NAME: Database name.

    Returns:
        mysql.connector.connection.MySQLConnection:
        A connection to the database.
    """
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    # Establish the database connection
    return mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name,
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
