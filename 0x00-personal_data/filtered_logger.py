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
