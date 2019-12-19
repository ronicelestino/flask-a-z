FROM python:3.7-buster

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    wget \
    python-dev \
    default-libmysqlclient-dev

ADD ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt



ADD ./app /app


