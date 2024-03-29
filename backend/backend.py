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


def resume_get(user_id, resume_id, cnx):
    """Получение резюме"""

    get_resume_query = """
    SELECT resume_title, resume_text 
    FROM resumes 
    WHERE (user_id=%s) AND (id=%s);
    """
    val_tuple = (
        user_id,
        resume_id,
    )
    try:
        with cnx.cursor() as cursor:
            cursor.execute(get_resume_query, val_tuple)
            result = cursor.fetchone()
            return result
    except errors.Error as err:
        print('Data receiving error for get resume!', '\n', err)
        return None


def resume_update(user_id, resume_id, resume_title, resume_text, cnx):
    """Редактирование резюме"""

    update_resume_query = """
    UPDATE resumes
    SET resume_title = %s, resume_text = %s
    WHERE (user_id=%s) AND (id=%s);
    """
    val_tuple = (
        resume_title,
        resume_text,
        user_id,
        resume_id,
    )
    try:
        with cnx.cursor() as cursor:
            cursor.execute(update_resume_query, val_tuple)
            cnx.commit()
            # получить маркер успешности операции
            return cursor.lastrowid
    except errors.Error as err:
        print('Data receiving error for get resume!', '\n', err)
        return None


def resume_delete(user_id, resume_id, cnx):
    """Удаление резюме"""

    delete_resume_query = """
    DELETE FROM resumes
    WHERE (user_id=%s) AND (id=%s);
    """
    val_tuple = (
        user_id,
        resume_id,
    )
    try:
        with cnx.cursor() as cursor:
            cursor.execute(delete_resume_query, val_tuple)
            cnx.commit()
            # получить маркер успешности операции
            return cursor.rowcount
    except errors.Error as err:
        print('Data receiving error for get resume!', '\n', err)
        return None
