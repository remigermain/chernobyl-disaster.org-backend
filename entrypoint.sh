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

# ------
# crontab
# ------
echo "* 0 * * * ./manage.py dbbackup --encrypt --clean --compress >/dev/null 2>&1 " > cronfile.txt
echo "* 0 * * * ./manage.py mediabackup --encrypt --clean --compress >/dev/null 2>&1 " >> cronfile.txt
echo "* 0 * * * ./manage.py locales_json >/dev/null 2>&1 " >> cronfile.txt
crontab cronfile.txt
cron -f


# exec command from docker-compose file
exec "$@"