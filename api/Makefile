all:
	./run_api.sh
clean:
	rm -f users.db
tunnel:
	./run_tunnel.sh
test:
	python3 -m pytest src/tests
	# running as module enforces absolute imports

build:
	sudo docker build . -t api-test
run: build
	sudo docker run api-test
re: clean all
