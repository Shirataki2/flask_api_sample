FROM mysql:8.0
EXPOSE 3306

RUN chown -R mysql /var/lib/mysql

RUN useradd -m docker
ENV HOME /home/docker
USER docker

ADD ./my.cnf /etc/mysql/conf.d/my.cnf

CMD [ "mysqld" ]