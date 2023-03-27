include .env

.PHONY: build up down restart test db-shell web-shell

ENV ?= dev
ifeq ($(ENV), dev)
	DEV_FILE = -f docker-compose.dev.yaml
endif
COMMAND = docker-compose -f docker-compose.prod.yaml $(DEV_FILE)

up build down restart :
	$(COMMAND) $@ &

test :
	$(COMMAND) exec backend python3 -m pytest /app/tests

db-shell :
	$(COMMAND) exec database cqlsh -u cassandra -p cassandra

web-shell :
	$(COMMAND) exec backend bash
