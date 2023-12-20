""" Конструктор резюме """
import os
from mysql.connector import connect, errors
from flask import Flask, request, render_template, redirect
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required
import backend
import markdown
from dotenv import load_dotenv

load_dotenv()

connection_info = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", ""),
}


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


@app.context_processor
def inject_user_data():
    """Внедрение переменных в шаблон"""
    return dict(user_is_authenticated=current_user.is_authenticated)


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
            with connect(**connection_info) as connection:
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
            with connect(**connection_info) as connection:
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
            with connect(**connection_info) as connection:
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
        with connect(**connection_info) as connection:
            user_id = current_user.get_id_int()
            data = backend.resume_list(
                user_id, connection)
            if data is None:
                return render_template("list.html", resume_list_error=True)

    except errors.Error as err:
        print('Cannot connect to MySQL server', '\n', err)
        return render_template("list.html", resume_list_error=True)

    return render_template("list.html", resumes=data)


@login_required
@app.route("/resume/edit/<int:resume_id>", methods=['post', 'get'])
def resume_edit(resume_id):
    """Редактирование резюме"""

    if request.method == 'POST':
        resume_title = request.form.get('resume_title', '', str)
        resume_text = request.form.get('resume_text', '', str)
        # установка соединения с БД
        try:
            with connect(**connection_info) as connection:
                user_id = current_user.get_id_int()
                new_resume_id = backend.resume_update(
                    user_id, resume_id, resume_title, resume_text, connection)
                if new_resume_id is None:
                    return render_template("edit.html", resume_create_error=True)

        except errors.Error as err:
            print('Cannot connect to MySQL server', '\n', err)
            return render_template("edit.html", resume_create_error=True)

        return redirect('/resume/list')

    try:
        with connect(**connection_info) as connection:
            user_id = current_user.get_id_int()
            data = backend.resume_get(
                user_id, resume_id, connection)
            if resume_id is None:
                return render_template("list.html", get_resume_error=True)
            resume_title, resume_text = data
            return render_template("edit.html", resume_id=resume_id, resume_title=resume_title, resume_text=resume_text)

    except errors.Error as err:
        print('Cannot connect to MySQL server', '\n', err)
        return render_template("list.html", get_resume_error=True)


@login_required
@app.route("/resume/delete/<int:resume_id>", methods=['post'])
def resume_delete(resume_id):
    """Удаление резюме"""

    try:
        with connect(**connection_info) as connection:
            user_id = current_user.get_id_int()
            data = backend.resume_delete(
                user_id, resume_id, connection)
            if data is None:
                return render_template("list.html", delete_resume_error=True)

    except errors.Error as err:
        print('Cannot connect to MySQL server', '\n', err)
        return render_template("list.html", delete_resume_error=True)

    return redirect('/resume/list')


@login_required
@app.route("/resume/get/<int:resume_id>")
def resume_get(resume_id):
    """Получение резюме"""

    try:
        with connect(**connection_info) as connection:
            user_id = current_user.get_id_int()
            data = backend.resume_get(
                user_id, resume_id, connection)
            if data is None:
                return render_template("list.html", get_resume_error=True)
            resume_title, resume_text = data

    except errors.Error as err:
        print('Cannot connect to MySQL server', '\n', err)
        return render_template("list.html", get_resume_error=True)

    resume_text = markdown.markdown(resume_text, extensions=[
                                    'markdown.extensions.tables', 'markdown.extensions.fenced_code'])
    return render_template("view.html", resume_title=resume_title, resume_text=resume_text)
