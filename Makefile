#!make

build:
	# build main project image
	docker build -t equilator_api -f openapi/Dockerfile .

prune:
	# remove unused docker stuff
	docker system prune -f

run-db:
	# run compose db only
	docker-compose -f docker-compose.yml up --build equilator_api_db

run-dev:
	# run compose db and openapi using python
	docker-compose -f docker-compose.yml up --build equilator_api_db

run-all: build prune
	# build run project locally without daemon
	docker-compose -f docker-compose.yml up --build

migrations:
	# creates new migrations
	alembic revision --autogenerate -m "init"

migrate:
	# upgrade DB schema to last migration
	alembic upgrade head

tests: build prune
	# build images, prune data and run tests
	docker-compose -f docker-compose.test.yml up --exit-code-from equilator_api_test
