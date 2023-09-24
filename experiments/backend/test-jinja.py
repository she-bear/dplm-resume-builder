import jinja2
from jinja2 import Environment, FileSystemLoader
from flask import escape

# инициализация среды выполнения для шаблонов 
environment = Environment(loader=FileSystemLoader("templates/"), autoescape=True)
# загрузка шаблона body.html -> base.html
template = environment.get_template("body.html")

# визуализация шаблона
title = "Page title"
name = "John"
# расширение базового шаблона body.html -> base.html
print(template.render(title = title, name = name))

# HTML escape
template_string = '<div>Some HTML Content</div>'
print(escape(template_string))