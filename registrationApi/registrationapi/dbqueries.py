from mysql.connector import connection, errors
from registrationapi.exceptions import DatabaseError, DatabaseIntegrityError
import os
from config import get_config

DB_CONFIG = get_config().DB_CONFIG

def get_user_by_username(username):
    try:
        cnx = connection.MySQLConnection(**DB_CONFIG, buffered=True, connection_timeout=20)
        cursor = cnx.cursor()
        query = ("SELECT username, email, password FROM client "
            "WHERE username = '%s';"%(username))
        cursor.execute(query)
        results = [asset for asset in cursor]
        cursor.close()
        cnx.close()
        return results[0] if len(results) > 0 else None
    except errors.Error as err:
        raise DatabaseError(err.msg)

def get_user_by_email(email):
    try:
        cnx = connection.MySQLConnection(**DB_CONFIG, buffered=True, connection_timeout=20)
        cursor = cnx.cursor()
        query = ("SELECT username, email, password FROM client "
            "WHERE email = '%s';"%(email))
        cursor.execute(query)
        results = [asset for asset in cursor]
        cursor.close()
        cnx.close()
        return results[0] if len(results) > 0 else None
    except errors.Error as err:
        raise DatabaseError(err.msg)

def create_user(email, password, username=None):
    try:
        cnx = connection.MySQLConnection(**DB_CONFIG, buffered=True, connection_timeout=20)
        cursor = cnx.cursor()

        if not username:
            username=email

        query = ("INSERT INTO client "
                    "(username, email, password) "
                    "VALUES ('%s', '%s', '%s');"%(username, email, password))
        try:
            cursor.execute(query)
            cnx.commit()
        except errors.IntegrityError as err:
            raise DatabaseIntegrityError(err.msg)

        finally:
            cursor.close()
            cnx.close()

    except errors.Error as err:
        raise DatabaseError(err.msg)
