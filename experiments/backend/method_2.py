from flask import Flask, request, render_template, redirect
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user

app = Flask(__name__)

database_id = 1
database = [{
            'title': 'Title 1',
            'id': 0,
            },
            {
            'title': 'Title 2',
            'id': 1,
            }]

def fetch_database():
    return database

def add_database(title):
    global database_id
    database_id+=1
    database.append({'title': title, 'id': len(database)})

def del_database(id):
    for i in range(len(database)):
        if database[i]['id'] == id:
            database.pop(i)
            break

@app.route('/api/list')
def route_index():
    data = fetch_database()
    return data


@app.route('/api/todo', methods=['PUT', 'DELETE'])
def route_add():
    if request.method == 'PUT':
        title = request.json.get('title', '')
        add_database(title)
    else:
        # здесь нужна проверка id
        id = request.json.get('id', 0)
        del_database(id)
    return {'status': 'ok'}

    


