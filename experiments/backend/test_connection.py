from getpass import getpass
from mysql.connector import connect, Error

import os

db_host = os.getenv("MYSQL_HOST", "localhost")
db_user = os.getenv("MYSQL_USER", "root")
db_password = os.getenv("MYSQL_PASSWORD", "")
db_name = os.getenv("MYSQL_DATABASE", "")

try:
    with connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    ) as connection:
        # запрос на добавление пользователя
        user_login = input("Enter user login: ")
        user_pwd = getpass("Enter user password: ")
        insert_user_query = """
        INSERT users
        VALUES
            (DEFAULT, %s, %s)
        """ 
        val_tuple = (
            user_login,
            user_pwd,
        )
        with connection.cursor() as cursor:
            cursor.execute(insert_user_query, val_tuple)
            connection.commit()
            # получить ID пользователя
            print(cursor.lastrowid)
except Error as e:
    print(e)