FROM python:3.7-slim

ENV app=/var/www

ADD . $app
WORKDIR $app

RUN pip install -r $app/requirements.txt