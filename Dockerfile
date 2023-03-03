FROM python:3.12-rc-alpine3.16

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 6379 5432

ENTRYPOINT [ "python", "app.py" ]