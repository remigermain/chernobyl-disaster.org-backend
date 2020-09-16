FROM python:3.8.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#postgre
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# for pillow
RUN apk add zlib-dev jpeg-dev

RUN pip install --upgrade pip

COPY ./requirements/common.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . .

RUN export $(cat .env | xargs) && ./manage.py migrate --no-input
RUN export $(cat .env | xargs) && ./manage.py collectstatic --no-input --clear --link