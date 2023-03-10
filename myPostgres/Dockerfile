FROM postgres:14.3

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD mypasswd
ENV POSTGRES_DB database

ADD createTables.sql /docker-entrypoint-initdb.d/