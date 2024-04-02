all: up

DOCKER := sudo docker

up:
	${DOCKER} compose up -d
upbuild:
	${DOCKER} compose up --build -d
down:
	${DOCKER} compose down
fdown:
	${DOCKER} compose down -v
stop:
	${DOCKER} compose stop
start:
	${DOCKER} compose start
ps:
	${DOCKER} compose ps

debug: fdown
	${DOCKER} compose -f docker-compose.debug.yaml up --build -d

logs:
	${DOCKER} compose logs

to_nginx:
	${DOCKER} exec -it nginx /bin/bash

clean: down
	-${DOCKER} down -v
	-${DOCKER} stop $$(${DOCKER} ps -aq)
	-${DOCKER} rm $$(${DOCKER} ps -aq)
fclean: clean
	yes 'y' | ${DOCKER} system prune -a
	yes 'y' | ${DOCKER} builder prune -a


logsf:
	${DOCKER} compose logs --follow
