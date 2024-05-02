all: up

DOCKER := sudo docker
COMPOSE := ${DOCKER} compose

up:
	${COMPOSE} up -d 

upd: upbuild
upbuild:
	${COMPOSE} up --build -d
down:
	${COMPOSE} down
fdown:
	${COMPOSE} down -v
stop:
	${COMPOSE} stop
start:
	${COMPOSE} start
rawdog:
	${COMPOSE} up --build --no-cache -d
ps:
	${COMPOSE} ps

logs:
	${COMPOSE} logs

to_nginx:
	-${COMPOSE} exec -it nginx /bin/bash
to_api:
	-${COMPOSE} exec -it api /bin/sh

clean: down
	-${COMPOSE} down -v
	-${COMPOSE} stop $$(${COMPOSE} ps -aq)
	-${COMPOSE} rm $$(${COMPOSE} ps -aq)
bclean:
	yes 'y' | ${DOCKER} builder prune -a
fclean: clean bclean
	yes 'y' | ${DOCKER} system prune -a

re: clean all

images:
	${COMPOSE} image ls

logsf:
	${COMPOSE} logs --follow
