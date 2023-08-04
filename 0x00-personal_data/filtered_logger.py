#!/usr/bin/env python3
"""
This script contain 'filter_datum' that returns the log message obfuscated:

Arguments:
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating all
    fields in the log line (message) {i}=.+?{separator}
 e.g email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;
 to email=eggmin@eggsample.com;password=xxx;date_of_birth=xxx;
"""
from typing import List
import re
import logging
from os import getenv
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    This function returns the log message obfuscated
    using the fields list
    """
    pattern = ''.join(["{}=.+?{}".format(i, separator) for i in fields])
    replace = separator.join(["{}={}".format(i, redaction)for i in fields])
    result = re.sub(pattern, replace + separator, message)
    return result


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ This constructor for this class. """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        ''' Returns a Log message. '''
        message = super(RedactingFormatter, self).format(record)
        output = filter_datum(self.fields, self.REDACTION,
                              message, self.SEPARATOR)
        return output


def get_logger() -> logging.Logger:
    """ This a Logger for sensitive fields. """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_logger = logging.StreamHandler()
    stream_logger.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_logger)
    logger.propagate = False
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ This function connect to the database. """
    username = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_host = getenv('PERSONAL_DATA_DB_HOST', "localhost")
    db_password = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_name = getenv('PERSONAL_DATA_DB_NAME')

    db_connect = mysql.connector.connect(user=username,
                                         password=db_password,
                                         host=db_host,
                                         port=3306,
                                         database=db_name)
    return db_connect
