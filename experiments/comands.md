### mySQL
docker run --name=mysql --env-file database/mysql.env -v ${PWD}/database/db_init.sql:/docker-entrypoint-initdb.d/db_init.sql -v resume-builder-volume:/var/lib/mysql -d -p 3306:3306 mysql

### backend
docker run -it --rm -p 9090:9090 backend

### ngnix
docker run -it --rm -v ./nginx/default.conf:/etc/nginx/conf.d/default.conf -p 80:80 nginx

### docker compose
docker compose up --build

```
опция --build запускает принудительную пересборку тех контейнеров, для которых указана собственная сборка (не через готовый image)
это нужно для того, чтобы в сборку попали последние обновления python-программы (в нашем случае backend)
если этой опции не будет, возьмёт существующий image от последней сборки
```
