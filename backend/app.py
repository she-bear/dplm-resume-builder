""" Конструктор резюме """
import os
from mysql.connector import connect, errors
from flask import Flask, request, render_template, redirect


db_host = os.getenv("MYSQL_HOST", "localhost")
db_user = os.getenv("MYSQL_USER", "root")
db_password = os.getenv("MYSQL_PASSWORD", "")
db_name = os.getenv("MYSQL_DATABASE", "")

app = Flask(__name__)


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


@app.route("/register", methods=['post', 'get'])
def register():
    """Обработка регистрации пользователя"""
    if request.method == 'POST':
        username = request.form.get('username', '', str)
        password = request.form.get('password', '', str)
        password_confirm = request.form.get('password_confirm', '', str)
        # проверка соответствия паролей
        if password != password_confirm:
            return render_template("register.html", password_dont_match=True)
        # установка соединения с БД
        try:
            with connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            ) as connection:
                user_id = user_add(username, password, connection)
                if user_id is None:
                    return render_template("register.html", registration_error=True)
                print("User added, ID =", user_id)
        except errors.Error as err:
            print('Cannot connect to MySQL server', '\n', err)
            return render_template("register.html", registration_error=True)

        return redirect('/resume/list')

    return render_template("register.html")
