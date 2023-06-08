## Запуск БД в docker

Для запуска mysql в Docker нужно создать контейнер при помощи команды: docker run <имя контейнера>

1. Запустить приложение Docker Desktop на Windows

2. https://hub.docker.com/_/mysql - документация

Демо-команда (запустить БД с доступом без пароля, удалить контейнер после окончания работы)
```
sudo docker run -d --rm -e MYSQL_ALLOW_EMPTY_PASSWORD=true -p 3306:3306 mysql
```

Запусть с root-паролем. В этом случае запуск из командной строки (docker exec -it mysql -p):
```
sudo docker run --name=mysql -e MYSQL_ROOT_PASSWORD=123 -d -p 3307:3306 mysql
```

Запустить контейнер и считать переменные среды из файла (имя файла произвольное, путь - относительно места запуска, в моем случае experiments/database/mysql.env):
```
sudo docker run --name=mysql --env-file mysql.env -d -p 3307:3306 mysql
```

Опции:
```
-d - запуск в режиме демона

--rm - удалить контейнер после использования (команда docker stop приведёт к УДАЛЕНИЮ контейнера!)

-e - установить переменные среды (https://docs.docker.com/engine/reference/run/#env-environment-variables)

-p - проброс портов (хост:контейнер)

--env-file - путь к файлу с переменными среды (см. список опций для docker run: https://docs.docker.com/engine/reference/commandline/run/)
```

3. Работа из командной строки
```
docker exec -it mysql
```

Войти и запросить пароль для root-пользователя (для случая с MYSQL_ROOT_PASSWORD=123):
```
docker exec -it mysql -p
```

Войти и запросить пароль для заданного пользователя (вариант с env-файлом):
```
docker exec -it mysql mysql -u <имя пользователя> -p
```

4. Чтение переменных среды из env-файла:

mysql.env
```
MYSQL_ALLOW_EMPTY_PASSWORD=yes
MYSQL_DATABASE=resume
MYSQL_USER=olgaK
MYSQL_PASSWORD=123
```

Пользователь с именем MYSQL_USER и паролем MYSQL_PASSWORD будет иметь доступ только к БД MYSQL_DATABASE.