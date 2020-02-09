FROM ubuntu:trusty
MAINTAINER ThaRising

RUN sudo apt-get -y update && sudo apt-get -y upgrade

RUN sudo apt-get install -y sqlite3 libsqlite3-dev && mkdir /db

RUN /usr/bin/sqlite3 /db/test.db

CMD /bin/bash
