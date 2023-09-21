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