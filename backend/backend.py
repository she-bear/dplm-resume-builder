"""Функции для работы с базой данных"""
from mysql.connector import errors


def user_add(user_login, user_pwd, cnx):
    """ Запрос на добавление пользователя (вернет int в случае успеха и None, если exception)"""

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
        return None


def user_login(user_login, cnx):
    """ Запрос на проверку существования пользователя (вернет int в случае успеха и None, если exception)"""

    get_user_query = """
    SELECT id, password FROM users WHERE login=%s;
    """
    val_tuple = (
        user_login,
    )
    try:
        with cnx.cursor() as cursor:
            cursor.execute(get_user_query, val_tuple)
            result = cursor.fetchone()
            return result
    except errors.Error as err:
        print('Data receiving error for login!', '\n', err)
        return None


def resume_create(user_id, resume_title, resume_text, cnx):
    """Создание резюме"""
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
        return None


def resume_list(user_id, cnx):
    """Получение списка резюме"""

    get_resume_query = """
    SELECT id, resume_title
    FROM resumes
    WHERE (user_id=%s);
    """
    val_tuple = (
        user_id,
    )
    try:
        with cnx.cursor() as cursor:
            cursor.execute(get_resume_query, val_tuple)
            result = cursor.fetchall()
            return result
    except errors.Error as err:
        print('Data receiving error for resume list!', '\n', err)
        return None
