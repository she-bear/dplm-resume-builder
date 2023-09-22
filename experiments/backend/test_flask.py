from flask import Flask, request
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user

# При наследовании от flask_login.UserMixin получаем доступ к методам и атрибутам, которые связаны с аутентификацией и авторизацией пользователей.
# Этот объект будет создаваться КАЖДЫЙ раз, при каждом запросе,
# т.е. ЛЮБОЙ route вызовет создание этого объекта
class UserSession(UserMixin):
    def __init__(self, userid):
        # создать объект пользователя по его ID
        self.id = userid

    # эта функция нужна flask, чтобы знать, какое число сохранить у пользователя на компьютере в cookies
    def get_id_init(self):
        return int(self.id)

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
# Ключ шифрования cookies
app.secret_key = 'secret key'

# login_manager.user_loader используется для загрузки пользователя из сессии при аутентификации. Принимает имя(id) пользователя в качестве аргумента и возвращает объект пользователя. Эта функция будет вызываться в каждом route!
@login_manager.user_loader
def load_user(user_id):
    return UserSession(user_id)

@app.route('/login')
def route_login():
    # здесь будет обращение к БД
    user_id = 123
    user_object = UserSession(user_id)
    # сохраняет информацию о пользователе в сессии и устанавливает переменную user_id
    login_user(user_object, remember = True)
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

@app.route("/")
def home():
    return "Hello World!"

@app.route('/json')
def get_json():
    return {"string value":"string field",
            "number value": 123}

@app.route('/req', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "POST request"
    else:
        return "GET request"

# получение любого аргумента из запроса, который идет после /url?<аргумент>    
@app.route('/url')
def get_query_string():
    return request.query_string

# получение целочисленного аргумента из запроса вида /url/<число>
@app.route('/url/<int:id>')
def show_id(id):
    return f'ID = {id}'

# получение логина и пароля
@app.route('/login', methods=['POST', 'GET'])
def get_user_login():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')
        return f'User = {user}, password = {password}'