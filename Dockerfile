FROM python:3.8.3-alpine

# create directory for the app user
RUN mkdir -p /var/www/backend

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/var/www/backend
ENV APP_HOME=/var/www/backend
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# for pillow / image kit
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add zlib-dev jpeg-dev libwebp libwebp-dev
RUN pip install --upgrade pip

COPY ./requirements/common.txt /requirements.txt
RUN pip install -r /requirements.txt

# copy entrypoint-prod.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.sh
ENTRYPOINT ["/var/www/backend/entrypoint.sh"]