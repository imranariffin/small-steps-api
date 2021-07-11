.PHONY: api

image_tag = small-steps-api-$(BUILD_ENV)

api:
	docker-compose --env-file .env.$(BUILD_ENV) up api

api_build:
	docker build -t $(image_tag) --build-arg BUILD_ENV=$(BUILD_ENV) ./api

api_build_nocache:
	docker build -t $(image_tag) --build-arg BUILD_ENV=$(BUILD_ENV) --no-cache ./api

api_bash:
	docker-compose --env-file .env.$(BUILD_ENV) \
		run \
		--rm \
		--name $(image_tag)-bash \
		--entrypoint /bin/bash \
		api

api_make_migrations:
	docker-compose --env-file .env.$(BUILD_ENV) \
		run \
		--rm \
		--name $(image_tag)-make-migrations \
		-e REVISION_NAME_SUFFIX=$(REVISION_NAME_SUFFIX) \
		--entrypoint ./entrypoints/make_migrations.sh \
		api \
		|| echo "Hint: Run make REVISION_NAME_SUFFIX=<you-revision-name-suffix> make_migrations"

api_run_migrations:
	docker-compose --env-file .env.$(BUILD_ENV) \
		run \
		--name $(image_tag)-run-migrations \
		--rm \
		run_migrations

api_run_tests:
	./scripts/check_build_env.sh test \
	&& docker-compose --env-file .env.$(BUILD_ENV) \
		run \
		--name small-steps-api-$(BUILD_ENV)-api \
		--rm \
		--entrypoint ./entrypoints/api.$(BUILD_ENV).sh \
		api
