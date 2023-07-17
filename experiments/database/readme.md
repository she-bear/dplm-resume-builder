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
sudo docker run --name=mysql -e MYSQL_ROOT_PASSWORD=123 -d -p 3307:3306 mysql
```

Запустить контейнер и считать переменные среды из файла (имя файла произвольное, путь - относительно места запуска):
```
sudo docker run --name=mysql --env-file experiments/database/mysql.env -d -p 3307:3306 mysql
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

[Документация по Where store data](https://hub.docker.com/_/mysql)

Создадим каталог вне контейнера и свяжем с папкой внутри контейнера.
Связь осуществляется через ключ -v:
```
-v /my/own/datadir:/var/lib/mysql
```

Что было сделано:
1. На хост-системе создана папка для хранения данных:
```
mkdir volume
```
2. Docker-контейнер запускался командой:
```
docker run --name=mysql --env-file experiments/database/mysql.env -v volume:/var/lib/mysql -d -p 3307:3306 mysql
```
3. Внутри БД была создана таблица users с данными:
```
sudo docker exec -it mysql mysql -u olgaK -p

USE resume;
CREATE TABLE users (id VARCHAR(10));
INSERT users (id) VALUES ('user1'), ('user2'), ('user3')

```
4. Затем остановили (docker stop) и удалили контейнер (docker rm).
5. Создали новый контейнер командой из пп.2, вошли в mysql и проверили, что данные сохранились:
```
mysql> select * from users;
+-------+
| id    |
+-------+
| user1 |
| user2 |
| user3 |
+-------+
```

### Эксперимент:

Создаем второй контейнер на другом порту:
```
docker run --name=mysql_copy --env-file experiments/database/mysql.env -v volume:/var/lib/mysql -d -p 3308:3306 mysql
```
Пытаемся зайти внутрь mysql - ошибка:
```
docker exec -it mysql_copy mysql -u olgaK -p
Enter password: 
ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)
```
Сейчас у нас два mysql-контейнера - на порту 3307 и на 3308:
```
docker ps -a
CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS              PORTS                               NAMES
30d8729814ef   mysql     "docker-entrypoint.s…"   About a minute ago   Up About a minute   33060/tcp, 0.0.0.0:3308->3306/tcp   mysql_copy
b6958801538e   mysql     "docker-entrypoint.s…"   20 minutes ago       Up 20 minutes       33060/tcp, 0.0.0.0:3307->3306/tcp   mysql
```
Останавливаем первый контейнер и убеждаемся, что через второй есть доступ к данным, которые хранятся во внешней папке volumes:
```
docker stop b6

docker exec -it mysql_copy mysql -u olgaK -p

USE resume;
SELECT * FROM users;
+-------+
| id    |
+-------+
| user1 |
| user2 |
| user3 |
+-------+
```

ЧТО НЕПОНЯТНО:
1. В случае разворачивания контейнера, как быть с "внешней" папкой? Нужно будет проверять её наличие и создавать, если такой папки нет? Кто будет этим заниматься?

2. Почему невозможен одновременный доступ к папке volumes из двух контейнеров? Как сделать, чтобы это было возможно?

3. Созданная папка volume - пуста, несмотря на то, что мы её связали с данными контейнера, добавили таблицу и данные в таблицу. Куда сохранились данные - загадка.


## Процедура подключения SQL Workbench

1. Запустить БД в контейнере (см. пп. Запуск БД в docker)

2. Запустить MySQL Workbench

3. На главном экране выбрать MySQL Connections, нажать + и задать параметры соединения с БД:
* Connection Method: Standard (TCP/IP)
* Host Name: 127.0.0.1
* Port (= в текущем примере 3307)
* User Name (root или заданный в параметре MYSQL_USER)

В случае успешного соединения в появившемся окне слева на вкладке Schemas можно получить доступ к БД и её таблицам.