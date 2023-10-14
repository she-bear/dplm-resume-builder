# передать данные param1=value1 param2=value2 четырьмя способами

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"

# здесь можно задать значения по умолчанию
# ожидаемый тип данных указывается в request.args.get
# https://werkzeug.palletsprojects.com/en/3.0.x/datastructures/#werkzeug.datastructures.MultiDict.get
# запрос вида http://127.0.0.1:5000/get_param?param1=2&param2=10
# тип передачи параметров: query
@app.route("/get_param")
def get_param():
  param1 = request.args.get("param1", 0, int)
  param2 = request.args.get("param2", 0, int)

  return f"param1: {param1}, param2: {param2}"

# для второго параметра задано значение по умолчанию
# запрос вида http://127.0.0.1:5000/url/2_10
# тип передачи параметров: path
@app.route('/url/<int:param1>',  defaults={'param2': 0})
@app.route('/url/<int:param1>_<int:param2>')
def show_id(param1, param2):
    return f"ID = {param1}, ID = {param2}"

# post form
# тип передачи параметров: body, тип кодирования: form
@app.route('/post_form', methods=['post', 'get'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username', '', str)
        password = request.form.get('password', '', str)
        message = f'Hello, {username} with password={password}!'
   
    return render_template('login.html', message = message)

# post json
# запрос: GET
# параметры: -
# ответ: html

# запрос: POST
# параметры body json: 
# - username : string
# - password : string
# ответ: json
#   "message" : string
@app.route('/post_json',  methods=['post', 'get'])
def post_json():
    if request.method == 'POST':
        username = request.json.get('username', '', str)
        password = request.json.get('password', '', str)
        message = f'Hello, {username} with password={password}!'
        return {"message" : message}
    
    return render_template('post_json.html')
