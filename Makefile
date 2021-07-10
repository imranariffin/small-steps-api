image_tag = small-steps-api-$(BUILD_ENV)

api:
	docker-compose --env-file .env.$(BUILD_ENV) up

build:
	docker build -t $(image_tag) --build-arg BUILD_ENV=$(BUILD_ENV) .

build_nocache:
	docker build -t $(image_tag) --build-arg BUILD_ENV=$(BUILD_ENV) --no-cache .

bash:
	docker-compose --env-file .env.$(BUILD_ENV) \
		exec \
		--rm \
		-it \
		--name $(image_tag)-bash \
		api \
		bash

make_migrations:
	docker-compose --env-file .env.$(BUILD_ENV) \
		run \
		--rm \
		--name $(image_tag)-make-migrations \
		-e REVISION_NAME_SUFFIX=$(REVISION_NAME_SUFFIX) \
		--entrypoint ./app/entrypoints/make_migrations.sh \
		api \
		|| echo "Hint: Run make REVISION_NAME_SUFFIX=<you-revision-name-suffix> make_migrations"

run_migrations:
	docker-compose --env-file .env.$(BUILD_ENV) \
		run \
		--name $(image_tag)-run-migrations \
		--rm \
		--entrypoint ./app/entrypoints/run_migrations.sh \
		api

run_tests:
	docker-compose --env-file .env.test \
		run \
		--name $(image_tag)-api \
		--rm \
		--entrypoint ./app/entrypoints/api.$(BUILD_ENV).sh \
		api
