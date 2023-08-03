#!/usr/bin/env python3
"""
This script contain 'filter_datum' that returns the log message obfuscated:

Arguments:
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating all
    fields in the log line (message)
 e.g email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;
 to email=eggmin@eggsample.com;password=xxx;date_of_birth=xxx;
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    This function returns the log message obfuscated
    using the fields list
    """
    pattern = ''.join([f"{i}=.+?{separator}" for i in fields])
    replace = separator.join(["{}={}".format(i, redaction)for i in fields])
    result = re.sub(pattern, replace + separator, message)
    return result
