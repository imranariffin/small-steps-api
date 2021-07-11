#!/bin/bash

BUILD_ENV_EXPECTED="production"
if [ $BUILD_ENV != $BUILD_ENV_EXPECTED ];
then
  echo "Wrong BUILD_ENV=$BUILD_ENV. Must be BUILD_ENV=$BUILD_ENV_EXPECTED"
  exit 1
fi

python ./scripts/pre_api.py \
  && echo "Successfully prepared api" \
  || (echo "Error during api preparation" && exit 1)

echo "Launching api over uvicorn ..."
uvicorn main:api --host 0.0.0.0 --port 8000
