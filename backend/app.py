""" Конструктор резюме """
import os
from mysql.connector import connect, errors
from flask import Flask, request, render_template, redirect
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required
import backend


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

    def get_id_int(self):
        """Какое число сохранить у пользователя на компьютере в cookies"""
        return int(self.id)


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
# Ключ шифрования cookies
app.secret_key = os.getenv("SECRET_KEY", "secret key")


@login_manager.user_loader
def load_user(user_id):
    """Загрузка пользователя из сессии при аутентификации.
    Принимает имя(id) пользователя в качестве аргумента и возвращает объект пользователя. Функция вызывается в каждом route."""
    return UserSession(user_id)


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
                user_id = backend.user_add(username, password, connection)
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
                user_data = backend.user_login(username, connection)
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


@login_required
@app.route("/resume/create", methods=['post', 'get'])
def resume_create():
    """Создание резюме"""
    if request.method == 'POST':
        resume_title = request.form.get('resume_title', '', str)
        resume_text = request.form.get('resume_text', '', str)
        # установка соединения с БД
        try:
            with connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            ) as connection:
                user_id = current_user.get_id_int()
                resume_id = backend.resume_create(
                    user_id, resume_title, resume_text, connection)
                if resume_id is None:
                    return render_template("edit.html", resume_create_error=True)

        except errors.Error as err:
            print('Cannot connect to MySQL server', '\n', err)
            return render_template("edit.html", resume_create_error=True)

        return redirect('/resume/list')

    return render_template("edit.html")


@login_required
@app.route("/resume/list")
def resume_list():
    """Формирование списка резюме"""
    try:
        with connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        ) as connection:
            user_id = current_user.get_id_int()
            data = backend.resume_list(
                user_id, connection)
            print(data)
            if data is None:
                return render_template("list.html", resume_list_error=True)

    except errors.Error as err:
        print('Cannot connect to MySQL server', '\n', err)
        return render_template("list.html", resume_list_error=True)

    return render_template("list.html", resumes=data)
