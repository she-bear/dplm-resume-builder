from getpass import getpass
from mysql.connector import connect, Error

import os
import pprint

env_var = os.environ
print("User's Environment variable:")
pprint.pprint(dict(env_var), width = 1)

try:
    with connect(
        host="localhost",
        user=input("Имя пользователя: "),
        password=getpass("Пароль: "),
    ) as connection:
        print(connection)
except Error as e:
    print(e)