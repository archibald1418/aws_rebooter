#!/bin/bash

certbot revoke /etc/letsencrypt/live/${HOST}/cert.pem
