FROM python:3.12-rc-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && \
    apt-get install -y redis-tools && \
    rm -rf /var/lib/apt/lists/*


EXPOSE 6379 5432

ENTRYPOINT [ "python", "app.py" ]