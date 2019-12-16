FROM python:3.7-buster

ENV PYTHONUNBUFFERED 1

ADD ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /app

ADD ./app /app