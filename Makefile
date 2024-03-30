all: up

DOCKER := sudo docker

up:
	${DOCKER} compose up -d
upd:
	${DOCKER} compose up --build -d
down:
	${DOCKER} compose down
ps:
	${DOCKER} compose ps

logs:
	${DOCKER} compose logs

to_nginx:
	${DOCKER} exec -it nginx /bin/bash


logsf:
	${DOCKER} compose logs --follow
