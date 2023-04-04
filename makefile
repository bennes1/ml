include .env

.PHONY: up down stop restart test db-shell web-shell rebuild-db

ENV ?= dev
ifeq ($(ENV), dev)
	DEV_FILE = -f docker-compose.dev.yaml
endif
COMMAND = docker-compose -f docker-compose.prod.yaml $(DEV_FILE)

up : build
	$(COMMAND) $@

database/scripts/.testsetup.cql : database/scripts/setup.cql
	sed 's/tictactoe/test/g' database/scripts/setup.cql > database/scripts/.testsetup.cql

build : database/scripts/.testsetup.cql */Dockerfile backend/pytest.ini backend/conftest.py
	$(COMMAND) $@ && touch build

down stop restart :
	$(COMMAND) $@

test :
	$(COMMAND) exec backend python3 -m pytest /app/tests

db-shell :
	$(COMMAND) exec database cqlsh -u cassandra -p cassandra

web-shell :
	$(COMMAND) exec backend bash

rebuild-db : database/scripts/.testsetup.cql
	$(COMMAND) down && \
	docker volume rm ml_database && \
	$(COMMAND) up --build &
