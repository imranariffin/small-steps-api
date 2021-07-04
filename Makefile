build:
	docker build -t small-steps-api .

build_nocache:
	docker build -t small-steps-api --no-cache .

network:
	docker network create small-steps-api-network

local_bash:
	docker run \
		-it \
		--rm \
		--name small-steps-api-bash \
		--volume `pwd`/app:/home/appuser/app \
		--network small-steps-api-network \
		--entrypoint bash \
		small-steps-api

local:
	docker run \
		-it \
		--rm \
		--name small-steps-api \
		--publish 8000:8000 \
		--volume `pwd`/app:/home/appuser/app \
		--network small-steps-api-network \
		--env-file .env \
		--entrypoint ./app/scripts/api.local.sh \
		small-steps-api

db:
	docker run \
		--detach \
		--name small-steps-api-db \
		--network small-steps-api-network \
		--env-file .env \
		--publish 5432:5432 \
		postgres

create_db:
	docker run \
		-it \
		--rm \
		--name small-steps-api-create-db \
		--network small-steps-api-network \
		--env-file .env \
		--entrypoint createdb \
		postgres \
		$(PGDATABASE)

make_migrations:
	docker run \
		-it \
		--rm \
		--name small-steps-api-make-migrations \
		--volume `pwd`/app:/home/appuser/app \
		--network small-steps-api-network \
		--env-file .env \
		--env REVISION_NAME_SUFFIX=$(REVISION_NAME_SUFFIX) \
		--entrypoint ./app/scripts/makemigrations.sh \
		small-steps-api

run_migrations:
	docker run \
		-it \
		--rm \
		--name small-steps-api-run-migrations \
		--volume `pwd`/app:/home/appuser/app \
		--network small-steps-api-network \
		--env-file .env \
		--entrypoint ./app/scripts/runmigrations.sh \
		small-steps-api
