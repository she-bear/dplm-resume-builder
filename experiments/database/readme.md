## Запуск БД в docker

Для запуска mysql в Docker нужно создать контейнер при помощи команды: docker run <имя контейнера>

1. Запустить приложение Docker Desktop на Windows

2. [Документация по mysql в docker](https://hub.docker.com/_/mysql)

Демо-команда (запустить БД с доступом без пароля, удалить контейнер после окончания работы)
```
sudo docker run -d --rm -e MYSQL_ALLOW_EMPTY_PASSWORD=true -p 3306:3306 mysql
```

Запусть с root-паролем. В этом случае запуск из командной строки (docker exec -it mysql -p):
```
sudo docker run --name=mysql -e MYSQL_ROOT_PASSWORD=123 -d -p 3306:3306 mysql
```

Запустить контейнер и считать переменные среды из файла (имя файла произвольное, путь - относительно места запуска):
```
sudo docker run --name=mysql --env-file experiments/database/mysql.env -d -p 3306:3306 mysql
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


## Volumes для хранения данных

[Документация по Where to store data](https://hub.docker.com/_/mysql)

![Alt text](https://docs.docker.com/storage/images/types-of-mounts-volume.png)

Существует два способа хранения данных для mysql, запущенного в docker-контейнере:
* bind mount - монтирование каталога с хоста. Файл с данными хранится на хосте (в существующем каталоге) и открывается внутри контейнера;
* volume - данные сохраняются в именованный том, который располагается в определенном каталоге docker на хостовой машине и не удаляется при удалении контейнера. Том может быть подключен к нескольким контейнерам.

Для решения нашей задачи будем использовать способ с volume (этот способ не требует дополнительных забот с внешней папкой - проверки прав доступа, например).



Что было сделано:
1. Усвоено что такое volume docker-контейнера и чем от отличается от внешней папки для хранения данных;

2. Docker-контейнер теперь запускается командой:
```
docker run --name=mysql --env-file experiments/database/mysql.env -v resume-builder-volume:/var/lib/mysql -d -p 3306:3306 mysql
```
Проверим, что docker-volume создан:
```
docker volume ls
DRIVER    VOLUME NAME
local     resume-builder-volume
```

3. Внутри БД была создана таблица users с данными:
```
sudo docker exec -it mysql mysql -u olgaK -p

USE resume;
CREATE TABLE users (id VARCHAR(10));
INSERT users (id) VALUES ('user1'), ('user2'), ('user3');

SELECT * FROM users;
+-------+
| id    |
+-------+
| user1 |
| user2 |
| user3 |
+-------+

```
4. Затем остановили контейнер (docker stop);

5. Создали новый контейнер командой из пп. 2, вошли в mysql и проверили, что данные сохранились:
```
mysql> SELECT * FROM users;
+-------+
| id    |
+-------+
| user1 |
| user2 |
| user3 |
+-------+
```


## Процедура подключения SQL Workbench

1. Запустить БД в контейнере (см. пп. Запуск БД в docker)

2. Запустить MySQL Workbench

3. На главном экране выбрать MySQL Connections, нажать + и задать параметры соединения с БД:
* Connection Method: Standard (TCP/IP)
* Host Name: 127.0.0.1
* Port (= в текущем примере 3306)
* User Name (root или заданный в параметре MYSQL_USER)

В случае успешного соединения в появившемся окне слева на вкладке Schemas можно получить доступ к БД и её таблицам.