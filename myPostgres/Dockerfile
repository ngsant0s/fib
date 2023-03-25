FROM postgres:13.4

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD mypasswd
ENV POSTGRES_DB database

COPY init.sql /docker-entrypoint-initdb.d/