#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done
echo "postgres started"


# import gpg keys for backup
GPG_PATH=gpg_keys
for KEY in $(ls -1 $GPG_PATH); do
	gpg --import "$GPG_PATH$KEY"
	echo "ADD pgp keys $KEY"
done

echo "migrate..."
./manage.py migrate --no-input
echo "collect static..."
./manage.py collectstatic --no-input --clear --link
echo "fix commit..."
./manage.py fix_commit
echo "generate images..."
./manage.py generateimages


# exec command from docker-compose file
exec "$@"
