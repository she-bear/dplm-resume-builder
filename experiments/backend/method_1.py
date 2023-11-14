from flask import Flask, request, render_template, redirect
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user

app = Flask(__name__)

database_id = 1
database = [{
            'title': 'Title 1',
            'id': 0,
            'done': False,
            },
            {
            'title': 'Title 2',
            'id': 1,
            'done': False,
            }]

def fetch_database():
    return database

def add_database(title):
    global database_id
    database_id+=1
    database.append({'title': title, 'id': len(database), 'done': False})

def del_database(id):
    for i in range(len(database)):
        if database[i]['id'] == id:
            database.pop(i)
            break

# 2. При любом смене route будет перезагрузка полная страницы
@app.route('/')
def route_index():
    data = fetch_database()
    return render_template('m1_index.html', data = data)


@app.route('/add', methods=['POST'])
def route_add():
    title = request.form.get('title', '', str)
    add_database(title)
    data = fetch_database()
    return render_template('ul.html', data = data)

# 3. необходима проверка id
# 1. delete должен быть post-запросом
# трудно делать на html (на каждом элементе д.б. form)
@app.route('/delete/<int:id>', methods=['DELETE'])
def route_delete(id):
    del_database(id)
    data = fetch_database()
    return render_template('ul.html', data = data)

    


