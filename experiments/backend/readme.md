# Настройки среды
## Обновление пакетов для WSL
```
sudo apt update
sudo apt upgrade
python3 --version
>> Python 3.10.12
```

## Установка расширения для VSCode
Python Microsoft

## Установка PIP
PIP (Python Package Index) - это менеджер пакетов Python, который позволяет устанавливать, обновлять и удалять пакеты Python. PIP используется для установки пакетов из репозиториев пакетов.

```
sudo apt install python3-pip
```

## Установка и настройка виртуального окружения .venv
 
[Инструкция](https://learn.microsoft.com/ru-ru/windows/python/web-frameworks)

**Venv (Virtual Environment)** - это виртуальное окружение, которое создается для изоляции среды разработки от других проектов и зависимостей. Оно позволяет создавать отдельные среды для каждого проекта и устанавливать только нужные пакеты и зависимости.

### Настройка виртуального окружения через VSCode
1. В корневой (!!!) папке проекта (в нашем случае в папке **~/dplm-resume-builder**) выполняем следующие команды:

Установка venv:
```
sudo apt install python3-venv
```

Cоздать виртуальную среду с именем .venv (в корневой папке появится папка .venv):
```
python3 -m venv .venv
```

Активировать виртуальную среду. При срабатывании перед командной строкой появится (.venv):
```
source .venv/bin/activate
```
Отключение виртуальной среды:
```
deactivate
```

2. Установить MySQL Connector

В текущей виртуальной среде (убедиться, что перед командной строкой появилось (.venv)) выполнить команду:
```
pip install mysql-connector-python
```
![](figures/venv_fig.png)

3. Экспортировать данные для входа (адрес, user, пароль) из переменных окружения

В папке .venv/bin/ находим файл activate:
![](figures/activate_fig.png)

В файл activate добавляем экспорт переменных среды:
```
export MYSQL_HOST=localhost
export MYSQL_USER=olgaK
export MYSQL_PASSWORD=123
export MYSQL_DATABASE=resume
```
![](figures/export_fig.png)

Команда export экспортирует переменную в окружающую среду оболочки так, чтобы ее значение стало доступным для MySQL и других процессов.

В Python чтение переменных окружения осуществляется через os.environ object: [ссылка на документацию.](https://www.geeksforgeeks.org/python-os-environ-object/)

В отличие от прямого доступа к объекту, функция os.getenv не вызовет ошибки если нет переменной, а возьмет значение по умолчанию (если значение по умолчанию не указано, то None). [Подробнее...](https://docs.python.org/3/library/os.html#os.getenv)

### Запуск программы

Py-файл на выполнение можно запустить двумя способами: 
1. Выбрать интерпретатор для py-файлов для запуска через VSCode

* переключиться на py-файл
* в VSCode внизу справа выбрать Select Interpreter

![](figures/select_fig.png)
* выбрать интерпретатор

![](figures/interp_fig.png)

Теперь, при нажатии на кнопку Play в py-файле активация виртуального окружения с нужными переменными и установленным MySQL Connector будет происходить автоматически.

2. Запустить из командной строки

* активировать виртуальное окружение:
```
source .venv/bin/activate
```

* в командной строке:
```
python experiments/backend/test_connection.py
```
![](figures/cline_fig.png)

## Ошибки

DatabaseError - Can't connect to MySQL server
IntegrityError - Duplicate entry 


## Запрос на добавление пользователя

Особенностью формирования запросов к БД является то, что нельзя добавлять значения запроса, предоставленные пользователем, напрямую в строку запроса, это влечёт неучтойчивость к SQL-инъекции. Лучше отправлять значения запроса в качестве аргументов в .execute().

Неверно:
```
        user_login = input("Enter user login: ")
        user_pwd = getpass("Enter user password: ")
        insert_user_query = """
        INSERT users
        VALUES
            (DEFAULT, "%s", "%s")
        """ % (
            user_login,
            user_pwd,
        )
        with connection.cursor() as cursor:
            cursor.execute(insert_user_query)
            connection.commit()
```

Самый простой способ:
```
        user_login = input("Enter user login: ")
        user_pwd = getpass("Enter user password: ")
        insert_user_query = """
        INSERT users
        VALUES
            (DEFAULT, %s, %s)
        """ 
        val_tuple = (
            user_login,
            user_pwd,
        )
        with connection.cursor() as cursor:
            cursor.execute(insert_user_query, val_tuple)
            connection.commit()
```

[Про SQL-инъекции](https://realpython.com/prevent-python-sql-injection/)

После того, как пользователь добавлен, необходимо получить его ID. В нашем случае это можно сделать не через прямой запрос, а через объект cursor:
```
cursor.lastrowid
``` 

Также в объекте cursor есть поле rowcount - сколько строк добавлено/найдено/изменено.