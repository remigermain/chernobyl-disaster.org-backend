#!/bin/ash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

./manage.py migrate --no-input
./manage.py collectstatic --no-input --clear --link
./manage.py loaddata data.json
./manage.py generateimages