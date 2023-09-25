"""Минимальный пример Flask-Login

Flask-login надежно сохраняет user id в cookies клиента.
Последующе запросы получают доступ к объекту UserSession, созданному из этого ID.

Демонстрация.

1. /login установит cookies с user_id = 123
2. /status покажет что юзер залогинен, user_id из cookies
3. /logout выход пользователя
4. /status покажет что пользователь не залогинен
"""

from flask import Flask
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user

class UserSession(UserMixin):
    """Модуль работы с пользователем"""
    def __init__(self, userid):
        """Создать объект пользователя из ID. 
        
        В реальном проекте может выполнять запрос к базе данных, 
        что бы получить дополнительную информацию.
        """
        self.id = userid

    def get_id_int(self):
        """Получить цисло user-id из класса"""
        return int(self.id)


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
# Ключ шифрования cookies
app.secret_key = 'secret key'

@login_manager.user_loader
def load_user(user_id):
    """Функция, которя создает и заполняет объект UserSession по user_id"""
    print("load user")
    return UserSession(user_id)

@app.route('/login')
def route_login():
    user_id = 123
    user_object = UserSession(user_id)
    login_user(user_object, remember=True)
    return "Login"

@app.route('/logout')
def route_logout():
    logout_user()
    return "Logout"

@app.route('/status')
def route_status():
    print("route status")
    # переменная current_user будет создана самим flask после
    # проверки cookies - есть такая сессия или нет
    if current_user.is_authenticated:
        user_id = current_user.get_id_int()
        return f"authenticated user_id={user_id}"
    else:
        return "not authenticated"