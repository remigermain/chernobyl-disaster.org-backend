FROM python:alpine

# ------
# python env
# ------
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# # ------
# # create dir
# # ------
RUN mkdir -p logs backup gpg_keys
# ENV HOME=/var/www/backend
# RUN mkdir -p $HOME $HOME/media $HOME/static
# RUN touch $HOME/django.log

# WORKDIR $HOME

# ------
# install app
# ------
# update
RUN apk update
# add postgre
RUN apk add postgresql-dev postgresql-client gcc python3-dev musl-dev
# add gnupgp for backup
RUN apk add gnupg
# for pillow / image kit
RUN apk add zlib-dev jpeg-dev libwebp libwebp-dev
# utils
RUN apk add bash

# ------
# install pip
# ------
RUN pip install --upgrade pip
COPY ./requirements/common.txt /requirements.txt
RUN pip install -r /requirements.txt

# ------
# copy DIR
# ------
COPY . .

ENTRYPOINT [ "./entrypoint.sh" ]
