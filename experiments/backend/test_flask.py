from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"

@app.route('/json')
def get_json():
    return {"string value":"string field",
            "number value": 123}