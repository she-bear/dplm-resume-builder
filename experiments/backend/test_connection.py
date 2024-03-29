from getpass import getpass
from mysql.connector import connect, errors

import os
import sys

# запрос на добавление пользователя (вернет int в случае успеха и None, если exception)
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
    except errors.Error as err:
        print('Data insertion error for user ', user_login, '\n', err)


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
            return cursor.lastrowid
    except errors.Error as err:
        print('Data insertion error, resume for user ', user_login, '\n', err)

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
            return result
    except errors.Error as err:
        print('Data receiving error for resume!', '\n', err)

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
            return result
    except errors.Error as err:
        print('Data receiving error for resume list!', '\n', err)

# удалить все резюме пользователя
def delete_resume_list(user_id, cnx):
    delete_resume_list_query = """
    DELETE
    FROM resumes
    WHERE (user_id=%s)
    """
    val_tuple = (
        user_id,
    )
    try:
        with cnx.cursor() as cursor:
            cursor.execute(delete_resume_list_query, val_tuple)
            cnx.commit()
            return cursor.rowcount
    except errors.Error as err:
        print('Data deleting error for resume list!', '\n', err)

# удалить пользователя
def delete_user(user_id, cnx):
    delete_user_query = """
    DELETE
    FROM users
    WHERE (id=%s)
    """
    val_tuple = (
        user_id,
    )
    try:
        with cnx.cursor() as cursor:
            cursor.execute(delete_user_query, val_tuple)
            cnx.commit()
            return cursor.rowcount
    except errors.Error as err:
        print('User deletion error, ID =', user_id, '\n', err)


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
            print("User added, ID =", user_id)
            
        resume_title = input("Enter resume title: ")
        resume_text = input("Enter resume text: ")
        resume_id = create_resume(user_id, resume_title, resume_text, connection)
        if resume_id == None:
            sys.exit(1)
        else: 
            print("Resume added, ID = ", resume_id)

        data = get_resume(user_id, resume_id, connection)
        if data == None:
            sys.exit(1)
        elif len(data) == 0:
            print('Cannot recieve any resume data!')
        else:
            for row in data:
                print (row)

        data = get_resume_list(user_id, connection)
        if data == None:
            sys.exit(1)
        elif len(data) == 0: 
            print('Cannot recieve any resume data!')
        else:
            for row in data:
                print (row)

        row_count = delete_resume_list(user_id, connection)
        if row_count == None:
            sys.exit(1)
        elif row_count == 0:
            print("There aren't resume for user ID =", user_id)
        else: 
            print("Resumes deleted, count = ", row_count)

        row_count = delete_user(user_id, connection)
        if row_count == None:
            sys.exit(1)
        elif row_count == 0:
            print("There isn't user ID =", user_id)
        else:
            print("User ID =", user_id, "deleted!")
  
except errors.Error as err:
    print('Cannot connect to MySQL server', '\n', err)