from getpass import getpass
from mysql.connector import connect, Error

import os

# запрос на добавление пользователя
def user_add():
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
    return insert_user_query, val_tuple

# создать резюме
def create_resume(user_id):
    resume_title = input("Enter resume title: ")
    resume_text = input("Enter resume text: ")
    create_resume_query = """
    INSERT resumes 
    VALUES
        (DEFAULT, %s, %s, %s);
    """
    val_tuple = (
        user_id,
        resume_title,
        resume_text,
    )
    return create_resume_query, val_tuple


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
        print(connection)
        with connection.cursor() as cursor:
            query, tuple = user_add()
            cursor.execute(query, tuple)
            connection.commit()
            # получить ID пользователя
            user_id = cursor.lastrowid
            # здесь анализ ошибки 

            query, tuple = create_resume(user_id)
            cursor.execute(query, tuple)
            connection.commit()
            # получить ID пользователя
            print(cursor.rowcount)
            # здесь анализ ошибки
except Error as e:
    print(e)