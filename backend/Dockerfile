FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# открыть порт для доступа к backend-контейнеру по протоколу uWSGI (значение - по умолчанию)
EXPOSE 9090/tcp

CMD [ "uwsgi", "--ini", "app.ini" ]
