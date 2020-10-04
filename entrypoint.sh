#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
sleep 0.1
done
echo "postgres started"


echo "migrate..."
./manage.py migrate --no-input
echo "collect static..."
./manage.py collectstatic --no-input --clear --link
echo "loaddata..."
./manage.py loaddata data.json
echo "fix commit..."
./manage.py fix_commit
echo "generate images..."
./manage.py generateimages


# exec command from docker-compose file
exec "$@"