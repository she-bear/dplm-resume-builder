import jinja2
from jinja2 import Environment, FileSystemLoader

# инициализация среды выполнения для шаблонов 
environment = Environment(loader=FileSystemLoader("templates/"))
# загрузка шаблона
template = environment.get_template("index.html")

# визуализация шаблона
title = "Page title"
name = "John"
print(template.render(title = title, name = name))