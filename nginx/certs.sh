#!/bin/sh


FLAGS="--debug -v --nginx -d $HOST --register-unsafely-without-email"

if [ $BUILD = 'dev' ]; then
	FLAGS+= " --test-cert"
fi


if [ ! -d /etc/letsencrypt/live/$HOST ]; then
    envsubst '${HOST}' < template.conf > /etc/nginx/conf.d/default.conf;
    yes 'y' | certbot $FLAGS
	# TODO: test script with --staging
else
    echo 'Certs already installed'
fi

service nginx stop

echo 'Starting nginx...'
if ! nginx -g 'daemon off;'; then
    echo 'Nginx failed'
    echo 'keep-alive container'
    tail -f /dev/null
fi
