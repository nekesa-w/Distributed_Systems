# Makefile
.PHONY: build run stop clean

build:
	docker-compose build

run:
	docker-compose up -d

stop:
	docker-compose down

clean: stop
	docker system prune -f