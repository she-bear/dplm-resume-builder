from getpass import getpass
from mysql.connector import connect, errors

import os
import sys

# запрос на добавление пользователя
def user_add(user_login, user_pwd, cnx):
    
    insert_user_query = """
    INSERT users
    VALUES
        (DEFAULT, %s, %s)
    """ 
    val_tuple = (
        user_login,
        user_pwd,
    )
    try:
        with cnx.cursor() as cursor:
            cursor.execute(insert_user_query, val_tuple)
            cnx.commit()
            # получить ID пользователя
            return cursor.lastrowid
    except errors.IntegrityError:
        print('Duplicate entry ', user_login)


# создать резюме
def create_resume(user_id, resume_title, resume_text, cnx):
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
    try:
        with cnx.cursor() as cursor:
            cursor.execute(create_resume_query, val_tuple)
            cnx.commit()
            # получить маркер успешности операции
            return cursor.rowcount, cursor.lastrowid
    except errors:
        print('Data insertion error for user ', user_login)

# получить текст резюме
def get_resume(user_id, resume_id, cnx):
    get_resume_query = """
    SELECT id, resume_title, resume_text
    FROM resumes
    WHERE (user_id = %s) AND (id = %s)
    """
    val_tuple = (
        user_id,
        resume_id
    )
    try:
        with cnx.cursor() as cursor:
            cursor.execute(get_resume_query, val_tuple)
            result = cursor.fetchall()
            return len(result), result
    except errors:
        print('Data receiving error for resume!')

# получить все резюме пользователя
def get_resume_list(user_id, cnx):
    get_resume_list_query = """
    SELECT id, resume_title
    FROM resumes
    WHERE (user_id=%s)
    """
    val_tuple = (
        user_id,
    )
    try:
        with cnx.cursor() as cursor:
            cursor.execute(get_resume_list_query, val_tuple)
            result = cursor.fetchall()
            return len(result), result
    except errors:
        print('Data receiving error for resume list!')


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

        user_login = input("Enter user login: ")
        user_pwd = getpass("Enter user password: ")
        user_id = user_add(user_login, user_pwd, connection)
        if user_id == None:
            sys.exit(1)
        else:
            for row in data:
                print (row)

        resume_title = input("Enter resume title: ")
        resume_text = input("Enter resume text: ")
        row_count, resume_id = create_resume(user_id, resume_title, resume_text, connection)
        if row_count == None:
            sys.exit(1)
        else: 
            print("Resume added, ID = ", resume_id)

        row_count, data = get_resume(user_id, resume_id, connection)
        if row_count == 0:
            print('Cannot recieve resume data!')
            sys.exit(1)
        else:
            for row in data:
                print (row)

        row_count, data = get_resume_list(32, connection)
        if row_count == 0:
            print('Cannot recieve resume data!')
            sys.exit(1)
        else:
            for row in data:
                print (row)
  
except errors.DatabaseError:
    print('Cannot connect to MySQL server')