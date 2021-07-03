build:
	docker build -t small-steps-api .

build_nocache:
	docker build -t small-steps-api --no-cache .

local_bash:
	docker run \
		-it \
		--rm \
		--name small-steps-api \
		--publish 8000:8000 \
		--volume `pwd`/app:/home/appuser/app \
		--entrypoint bash \
		small-steps-api

local:
	docker run \
		-it \
		--rm \
		--name small-steps-api \
		--publish 8000:8000 \
		--volume `pwd`/app:/home/appuser/app \
		--entrypoint ./app/scripts/entrypoint.local.sh \
		small-steps-api
