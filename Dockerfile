FROM ubuntu:16.04
MAINTAINER ThaRising

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY /application /data/api/application
COPY app.py /data/api/wsgi.py
COPY requirements.txt /data/api/requirements.txt

RUN pip install -r /data/api/requirements.txt

COPY /venv/Lib/site-packages/flask_restplus/fields.py /usr/local/lib/python3.7/site-packages/flask_restplus/fields.py
COPY /venv/Lib/site-packages/flask_restplus/api.py /usr/local/lib/python3.7/site-packages/flask_restplus/api.py

WORKDIR /data/api/

ENTRYPOINT [ "python" ]

CMD [ "wsgi.py" ]
