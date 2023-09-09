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

Установка venv:
```
sudo apt install python3-venv
```

Cоздать виртуальную среду с именем .venv (команда выполняется в папке проекта!):
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

## Установка MySQL Connector
В текущей виртуальной среде выполнить команду:
```
pip install mysql-connector-python
```

## Получение данные для входа (адрес, user, пароль) из переменных окружения

Для обучающей версии необходимые переменные экспортирум через bash:
```
export MYSQL_HOST=localhost
export MYSQL_USER=olgaK
export MYSQL_PASSWORD=123
export MYSQL_DATABASE=resume
```
Команда export экспортирует переменную в окружающую среду оболочки так, чтобы ее значение стало доступным для MySQL и других процессов.

В Python чтение переменных окружения осуществляется через os.environ object: [ссылка на документацию](https://www.geeksforgeeks.org/python-os-environ-object/)

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