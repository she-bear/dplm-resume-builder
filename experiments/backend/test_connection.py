from getpass import getpass
from mysql.connector import connect, Error

import os

db_host = os.getenv("MYSQL_HOST", "localhost")
db_user = os.getenv("MYSQL_USER", "root")
db_password = os.getenv("MYSQL_PASSWORD", "")

try:
    with connect(
        host=db_host,
        user=db_user,
        password=db_password,
    ) as connection:
        print(connection)
except Error as e:
    print(e)