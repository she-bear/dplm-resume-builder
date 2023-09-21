from flask import Flask, jsonify, request
app = Flask(__name__)

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