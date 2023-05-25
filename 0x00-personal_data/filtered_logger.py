#!/usr/bin/env python3
"""Write a function called filter_datum that returns the log """
import logging
import re
from typing import List
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """this is the constructor"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """filtered incoming log records"""
        return filter_datum(
            self.fields, self.REDACTION, super().format(record),
            self.SEPARATOR)


def filter_datum(
        fields: List[str], redaction: str, message: str, seperator: str
        ) -> str:
    """Returns the log message obfuscated"""
    for field in fields:
        message = re.sub(f"{field}=.+?{seperator}",
                         f"{field}={redaction}{seperator}", message)
    return message


def get_logger() -> logging.Logger:
    """set format

    Returns:
        A new log with all the items. A logger object
    """
    log: logging.Logger = logging.getLogger('user_data')
    log.propagate = False

    log.setLevel(logging.INFO)

    handler: logging.Handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    log.addHandler(handler)

    return log


def get_db() -> mysql.connecter.connection.MySQLConnection:
    """Connect to db
    Returns:
        connection to db
    """
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    user = os.environ.get('PERSONAL_DATA_DB_USERNAME')
    pswd = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    db = os.environ.get('PERSONAL_DATA_DB_NAME', 'root')

    return mysql.connector.connect(
        host=host, username=user, password=pswd, database=db)


def main():
    """main function to be executed"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users;")
    for row in cursor.fetchall():
        message = f"name={row[0]}; " + \
                  f"email={row[1]}; " + \
                  f"phone={row[2]}; " + \
                  f"ssn={row[3]}; " + \
                  f"password={row[4]};"
        record = logging.LogRecord("my_logger", logging.INFO,
                                   None, None, message, None, None)
        formatter = RedactingFormatter(PII_FIELDS)
        formatter.format(record)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
