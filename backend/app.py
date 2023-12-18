
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/register", methods=['post', 'get'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '', str)
        password = request.form.get('password', '', str)
        password_confirm = request.form.get('password_confirm', '', str)
        print(username, password, password_confirm)
        return 'ok'

    else:
        return render_template("register.html")
