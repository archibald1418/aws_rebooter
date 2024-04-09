#!/bin/sh

if [ ! -d /etc/letsencrypt/live/$HOST ]; then
    envsubst '${HOST}' < template.conf > /etc/nginx/conf.d/default.conf;
    yes 'y' | certbot -v --nginx -d $HOST --register-unsafely-without-email
else
    echo 'Certs already installed'
fi

service nginx stop

if ! nginx -g 'daemon off;'; then
    echo 'Nginx failed'
    echo 'keep-alive container'
    tail -f /dev/null
fi
