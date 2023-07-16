FROM mysql:latest

RUN chown -R mysql:root /var/lib/mysql/

ARG MYSQL_DATABASE
ARG MYSQL_USER
ARG MYSQL_PASSWORD
ARG MYSQL_ROOT_PASSWORD

ENV MYSQL_DATABASE=my_company
ENV MYSQL_USER=john
ENV MYSQL_PASSWORD=123
ENV MYSQL_ROOT_PASSWORD=123

ADD my_company.sql /etc/mysql/my_company.sql

RUN sed -i 's/MYSQL_DATABASE/'$MYSQL_DATABASE'/g' /etc/mysql/my_company.sql
RUN cp /etc/mysql/my_company.sql /docker-entrypoint-initdb.d

EXPOSE 3306