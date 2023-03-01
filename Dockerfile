FROM python:slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && \
    apt-get install -y redis-tools && \
    rm -rf /var/lib/apt/lists/*

RUN python app_test.py

ENTRYPOINT [ "python", "./app.py" ]