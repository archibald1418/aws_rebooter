FROM debian:bookworm-slim
RUN apt update && apt install -y nginx certbot python3-certbot-nginx \
    iputils-ping net-tools procps gettext-base
WORKDIR /opt
COPY --chmod=u+x ./certs.sh ./template.conf .
ENTRYPOINT /opt/certs.sh
