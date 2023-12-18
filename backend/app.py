""" Конструктор резюме """
import os
from mysql.connector import connect, errors
from flask import Flask, request, render_template, redirect
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user


db_host = os.getenv("MYSQL_HOST", "localhost")
db_user = os.getenv("MYSQL_USER", "root")
db_password = os.getenv("MYSQL_PASSWORD", "")
db_name = os.getenv("MYSQL_DATABASE", "")


class UserSession(UserMixin):
    """При наследовании от flask_login.UserMixin получаем доступ к методам и атрибутам, которые связаны с аутентификацией и авторизацией пользователей.
    Этот объект будет создаваться КАЖДЫЙ раз, при каждом запросе, т.е. ЛЮБОЙ route вызовет создание этого объекта
    """

    def __init__(self, userid):
        """Создает объект пользователя по его ID"""
        self.id = userid

    def get_id_init(self):
        """Какое число сохранить у пользователя на компьютере в cookies"""
        return int(self.id)


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
# Ключ шифрования cookies
app.secret_key = 'secret key'


@login_manager.user_loader
def load_user(user_id):
    """Загрузка пользователя из сессии при аутентификации.
    Принимает имя(id) пользователя в качестве аргумента и возвращает объект пользователя. Функция вызывается в каждом route."""
    return UserSession(user_id)


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


@app.route("/")
def home():
    """Главная страница"""

    # переменная current_user будет создана самим flask после
    # проверки cookies - есть такая сессия или нет
    if current_user.is_authenticated:
        return redirect("/resume/list")

    return redirect("/login")


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
                user_object = UserSession(user_id)
                # сохраняет информацию о пользователе в сессии и устанавливает переменную user_id
                login_user(user_object, remember=True)
        except errors.Error as err:
            print('Cannot connect to MySQL server', '\n', err)
            return render_template("register.html", registration_error=True)

        return redirect('/resume/list')

    return render_template("register.html")


@app.route("/login", methods=['post', 'get'])
def login():
    """Обработка логина пользователя"""
    if request.method == 'POST':
        username = request.form.get('username', '', str)
        password = request.form.get('password', '', str)
        # установка соединения с БД
        try:
            with connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            ) as connection:
                user_data = user_login(username, connection)
                if user_data is None:
                    return render_template("login.html", user_not_found=True)
                user_id, user_password = user_data

                if password != user_password:
                    return render_template("login.html", incorrect_password=True)

                user_object = UserSession(user_id)
                # сохраняет информацию о пользователе в сессии и устанавливает переменную user_id
                login_user(user_object, remember=True)

        except errors.Error as err:
            print('Cannot connect to MySQL server', '\n', err)
            return render_template("login.html", login_error=True)

        return redirect('/resume/list')

    return render_template("login.html")


@app.route('/logout')
def route_logout():
    """Logout"""
    logout_user()
    return redirect("/")
