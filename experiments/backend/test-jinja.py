import jinja2
from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return template.render(title = title, name = name)

# инициализация среды выполнения для шаблонов 
environment = Environment(loader=FileSystemLoader("templates/"))
# загрузка шаблона body.html -> base.html
template = environment.get_template("body.html")

# визуализация шаблона
title = "Page title"
name = "John"
# расширение базового шаблона body.html -> base.html
print(template.render(title = title, name = name))
