FROM python:3.8.3-alpine

ENV HOME=/var/www/sites/cher/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#postgre
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements/common.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . .

RUN ./manage.py migrate --no-input
RUN ./manage.py collectstatic --no-input --clear --link

RUN mkdir $HOME/static $HOME/media
WORKDIR $HOME