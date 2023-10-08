base.html:
* html
    * head
    * body
        * header
        * content <- index.html, list.html, resume.html
        * footer
    
## Список всех страниц, с описанием и списком параметров

* URL
* Тип запроса GET/POST
* Список параметров
* Тип параметра (url или form)
* Нужен ли login для доступа (к конкретной странице)
* Имя html шаблона

1. Главная страница
"/"

GET

<без параметров>

URL

Login для доступа: не нужен

Шаблон: index.html


2. Страница регистрации
"/registration"

POST

<login, password>

FORM

Login для доступа: не нужен

Шаблон: registration.html

3. Страница входа
"/login"

POST

<login, password>

FORM

Login для доступа: не нужен

Шаблон: login.html

4. Создание резюме
"/create"

POST

<user_id, resume_title, resume_text>

FORM

Login для доступа: нужен

Шаблон: create.html


5. Редактирование резюме
"/edit"

POST

<user_id, resume_id, resume_title, resume_text>

FORM

Login для доступа: нужен

Шаблон: edit.html


6. Просмотр списка резюме
"/list"

GET

<user_id>

URL

Login для доступа: нужен

Шаблон: list.html


7. Просмотр готового резюме по ссылке

???