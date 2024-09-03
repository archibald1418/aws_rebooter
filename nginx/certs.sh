#!/bin/sh


FLAGS="--debug -v --nginx -d $HOST --register-unsafely-without-email"

if [ "$BUILD" == "dev" ]; then
	FLAGS="$FLAGS --test-cert";
	# http only..
fi


if [ ! -d /etc/letsencrypt/live/$HOST ]; then
    envsubst '${HOST}' < template.conf > /etc/nginx/conf.d/default.conf;
    yes 'y' | certbot $FLAGS;
	# --test-cert gets invalid cert, so can only test with http
	# letsencrypt has two limits: duplicate cert limit and cert limit
    # 10 certs for 3 hours..
else
    echo 'Certs already installed';
fi

service nginx stop

echo 'Starting nginx...'
if ! nginx -g 'daemon off;'; then
    echo 'Nginx failed';
    echo 'keep-alive container';
    tail -f /dev/null;
fi
