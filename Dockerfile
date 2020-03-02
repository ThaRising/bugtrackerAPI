FROM ubuntu:trusty
MAINTAINER ThaRising

COPY /application /data/api/application
COPY wsgi.py /data/api/wsgi.py
COPY requirements.txt /data/api/requirements.txt

RUN sudo apt-get -y update && sudo apt-get -y upgrade

RUN sudo apt-get install -y pip

RUN sudo pip install -r /data/api/requirements.txt

RUN sudo python3.7 /data/api/wsgi.py

CMD /bin/bash
