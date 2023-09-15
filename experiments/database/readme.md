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
Заменяем на (чтобы оставить root-доступ и не было доступа без пароля):
```
MYSQL_ROOT_PASSWORD=123
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

## Процедура доступа через клиент mysql

1. Запустить БД в контейнере (см. пп. Запуск БД в docker)

2. Команда:
```
sudo docker exec -it <имя контейнера> mysql -u <имя пользователя> -p
```
<имя пользователя> берётся из файла mysql.env, переменная MYSQL_USER

В нашем случае:
```
sudo docker exec -it mysql mysql -u olgaK -p
```

### Некоторые команды:

* Посмотреть список БД:
```
SHOW DATABASES;
```
* Подключиться к конкретной БД:
```
USE resume;
```
### Отправить sql-файл на выполнение
Можно заранее создать список sql-инструкций, а потом выполнить их одним блоком.

Существует два способа:
* скопировать sql-файл внутрь контейнера

[IF YOU ARE USING MYSQL INSIDE DOCKER](https://stackoverflow.com/questions/14684063/mysql-source-error-2)

Недостатком этого способа является то, что sql-файл будет скопирован внутрь контейнера один раз и если потребуется изменить файл, то операцию нужно будет повторить (нет автоматизации)
```
# запускаем контейнер
docker run --name=mysql --env-file experiments/database/mysql.env -d -p 3306:3306 mysql
# копируем файл внутрь контейнера
sudo docker cp  experiments/database/db_init.sql  mysql:/
# заходим внутрь контейнера
sudo docker exec -it mysql mysql -u olgaK -p
# запускаем файл на выполнение
mysql> source db_init.sql
```

* подключить файл через volume и запустить на выполнение из хостовой системы

[Initializing a fresh instance](https://hub.docker.com/_/mysql)
```
# создаем контейнер, подключаем sql-файл
# в папке /docker-entrypoint-initdb.d/ хранятся файлы, которые будут запущены при инициализации контейнера
# если файлов несколько, они будут исполнены в алфавитном порядке
docker run --name=mysql --env-file experiments/database/mysql.env -v ${PWD}/experiments/database/db_init.sql:/docker-entrypoint-initdb.d/db_init.sql -d -p 3306:3306 mysql


# запустить файл на выполнение из хостовой системы
mysql -P 3306 -h 127.0.0.1 -u olgaK -p < experiments/database/db_init.sql

# либо (аналогично) изнутри контейнера через bash
sudo docker exec -it mysql bash

bash-4.4# mysql < /docker-entrypoint-initdb.d/db_init.sql
```

> Нужно обратить внимание на то, что volume для хранения данных при использовании mysql в контейнере создается всегда, даже если явно не указан, например:
```
# в явном виде подключение volume не задано
docker run --name=mysql --env-file experiments/database/mysql.env  -d -p 3306:3306 mysql

docker volume ls
DRIVER    VOLUME NAME
local     6d642e917269eb9ee65eced8250a5aaf966ab7ad5b7b38ddeaf0b851528f92f6
```

### Мы будем использовать способ, при котором sql-файл запускается автоматически при создании контейнера

```
docker run --name=mysql --env-file experiments/database/mysql.env -v ${PWD}/experiments/database/db_init.sql:/docke
r-entrypoint-initdb.d/db_init.sql -d -p 3306:3306 mysql
```

На данном этапе работы команда создания контейнера будет выглядеть следующим образом:
```
docker run --name=mysql --env-file experiments/database/mysql.env -v ${PWD}/experiments/database/db_init.sql:/docker-entrypoint-initdb.d/db_init.sql -v resume-builder-volume:/var/lib/mysql -d -p 3306:3306 mysql
```

## Файл инициализации БД (минимальный)
Для инициализации БД будем использовать файл db_init.sql

```
USE resume;

CREATE TABLE IF NOT EXISTS users(
    id int NOT NULL AUTO_INCREMENT,
    login varchar(255) UNIQUE NOT NULL,
    password varchar(255) NOT NULL,
    PRIMARY KEY(id)
);
```

## Запросы к БД (пользователь)
### Создание пользователя

```
INSERT users(login, password) VALUES ("user", "psw");
```
[Как вставлять данные в таблицы со столбцами AUTO_INCREMENT](https://stackoverflow.com/questions/8753371/how-to-insert-data-to-mysql-with-auto-incremented-columnfield)

Такие варианты тоже работают:
```
INSERT users VALUES(NULL, "user", "psw");
```
```
INSERT users VALUES(DEFAULT, "user", "psw");
```

При создании пользователя нужно получить его ID. Это делается командой:
```
SELECT LAST_INSERT_ID();
```
Важно понимать, что LAST_INSERT_ID() получит результат именно для ТЕКУЩЕЙ сессии.

[Ссылка на ответ](https://stackoverflow.com/a/15821655/292986)

### Проверка пароля
Получить пароль пользователя по его логину:
```
 SELECT password FROM users WHERE login="login";
```


## Запросы к базе данных (Резюме)
### Таблица резюме

```
CREATE TABLE IF NOT EXISTS resumes(
    id int NOT NULL AUTO_INCREMENT,
    user_id int NOT NULL,
    resume_title VARCHAR(100),
    resume_text TEXT,
    PRIMARY KEY(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Создание резюме
```
INSERT resumes 
VALUES(DEFAULT, users.user_id, "title", "text");
```

### Редактирование резюме
```
UPDATE resumes
SET resume_title = "new_title", resume_text = "new_text"
WHERE (user_id=current_user) AND (id=resume_id);
```

### Удаление резюме
```
DELETE FROM resums
WHERE (user_id=current_user) AND (id=resume_id);
```

### Получение текста резюме
```
SELECT id, resume_title, resume_text 
FROM resumes 
WHERE (user_id=current_user) AND (id=resume_id);
```
### Получение списка резюме
```
SELECT id, resume_title
FROM resumes
WHERE (user_id=current_user);
```

## Реализация каскадного удаления

Каскадное удаление в базах данных - это процесс, при котором удаляются связанные записи из других таблиц при удалении основной записи.
Реализуется с помощью механизма внешних ключей, который позволяет контролировать ссылочную целостность между таблицами.

В данной БД есть две таблицы - users (Пользователи) и resumes (Резюме), и одна запись пользователя может быть связана с несколькими резюме. При удалении пользователя из таблицы users **автоматически удаляются все связанные записи** этого пользователя из таблицы resumes.

Для реализации каскадного удаления в связанную таблицу необходимо добавить директиву:
```
ON DELETE CASCADE
```

Таким образом, на данном этапе работы файл инициализации БД db_init.sql будет иметь вид:
```
USE resume;

CREATE TABLE IF NOT EXISTS users(
    id int NOT NULL AUTO_INCREMENT,
    login varchar(255) UNIQUE NOT NULL,
    password varchar(255) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS resumes(
    id int NOT NULL AUTO_INCREMENT,
    user_id int NOT NULL,
    resume_title VARCHAR(100),
    resume_text TEXT,
    PRIMARY KEY(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
);
```
