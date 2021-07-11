# small-steps-api

## Local development

### Requirements

* docker >= 1.29.x
* docker-compose >= 20.10.x

### Run

```bash
# Set aliases
source ./aliases.sh

# Run tests
export BUILD_ENV=test && set_envs
make api_build
make api_run_tests

# Run application in a $BUILD_ENV cluster
export BUILD_ENV=dev && set_envs
make api_build
make api
# Now go to http://127.0.0.1:8000/
```

```bash
# Shutdown application (if needed)
dc down
# Make new migrations (if needed)
dc run api_make_migrations
# Run migrations (if needed)
dc run api_run_migrations
```
