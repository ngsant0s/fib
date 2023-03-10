FROM python:3.12.0a5

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "app.py" ]