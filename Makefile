build:
	docker build -t small-steps-api .

build_nocache:
	docker build -t small-steps-api --no-cache .
