## Структура шаблонов

base.html:
* html
    * head
    * body
        * header
        * content <- index.html, list.html, resume.html и т.д.
        * footer

## Список всех страниц, с описанием и списком параметров

1. Главная страница
"/"

```
запрос: GET
параметры: -
ответ: html
login для доступа: не нужен
```

Шаблон: index.html


2. Страница регистрации
"/register"

```
запрос: GET
параметры: -
ответ: html
login для доступа: не нужен
```

```
запрос: POST form
параметры (body):
            username: string
            password: string
            password_confirm: stringlogin
ответ:
            html (redirect?),
            message (ok, error)

login для доступа: не нужен
```

Шаблон: registration.html

3. Страница входа
"/login"

```
запрос: GET
параметры: -
ответ: html
login для доступа: не нужен
```

```
запрос: POST form
параметры (body):
            username: string
            password: string
ответ:
        html (redirect???)
        message (ok, error)

login для доступа: не нужен (???)
```

Шаблон: login.html

4. Создание резюме
"/resume/create"

```
запрос: GET
параметры: -
ответ: html
```

```
запрос: POST form
параметры (body):
            resume_title: string
            resume_text: string (markdown_string)
ответ:
            message (ok, error)

login для доступа: нужен
```

Шаблон: resume.html

5. Просмотр списка резюме
"/resume/list"

```
запрос: GET
параметры: -
ответ: html
login для доступа: нужен
```

Шаблон: list.html

6. Просмотр резюме
"/resume/view/<id:int>"

```
запрос: GET
параметры (path):
                id: int
ответ: html
login для доступа: нужен
```

Шаблон: view.html

7. Редактирование резюме
"/resume/edit/<id:int>"

```
запрос: GET
параметры (path):
                id: int
ответ: html
```

```
запрос: POST form
параметры (path):
                id: int
параметры (body):
            resume_title: string
            resume_text: string (markdown_string)
ответ:
            message (ok, error)

login для доступа: нужен            
```

Шаблон: resume.html

8. Удаление резюме
"/resume/delete/<id:int>"

```
запрос: POST
параметры (path):
                id: int
ответ:
            message (ok, error)

login для доступа: нужен 
```

9. Просмотр готового резюме по ссылке
"/resume/view/<id:int>"

```
запрос: GET
параметры: 
        id: int
ответ: html
```

Шаблон: view.html

## Запуск flask
```
flask --app app.py run
```
## Подключение и использование dotenv

https://ramziv.com/article/40

https://pypi.org/project/python-dotenv/

**python-dotenv** - это пакет, который считывает пары ключ-значение из файла .env, и загружает необходимые приложению переменные среды.

В нашем случае этот пакет будет использоваться, чтобы считать переменные среды для работой с базой данных.

1. Установка:
```
pip install python-dotenv
```

2. Затем выполняем pip freeze (чтобы обновился файл requirements.txt):
```
pip3 freeze > requirements.txt
```

3. В папке проекта создаем файл .env и переносим в него содержимое файла mysql.env.

4. Добавляем файл .env в .gitignore

5. Подключаем к проекту (app.py):
```
from dotenv import load_dotenv
load_dotenv()
```
