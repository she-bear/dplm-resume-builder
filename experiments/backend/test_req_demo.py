# передать данные param1=value1 param2=value2 четырьмя способами

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"

# здесь можно задать значения по умолчанию
# но нужно преобразование в int и проверка типов
# запрос вида http://127.0.0.1:5000/get_param?param1=2&param2=10
@app.route("/get_param")
def get_param():
  param1 = request.args.get("param1", 0)
  param2 = request.args.get("param2", 0)

  return f"param1: {param1}, param2: {param2}"

# для второго параметра задано значение по умолчанию
# запрос вида http://127.0.0.1:5000/url/2_10
@app.route('/url/<int:param1>',  defaults={'param2': 0})
@app.route('/url/<int:param1>_<int:param2>')
def show_id(param1, param2):
    return f"ID = {param1}, ID = {param2}"