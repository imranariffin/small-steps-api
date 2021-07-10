#!/bin/bash

if [ $BUILD_ENV != "dev" ];
then
  echo "Wrong BUILD_ENV=$BUILD_ENV. Must be BUILD_ENV=dev"
  exit 1
fi

python ./app/pre_api.py || (echo "Error during api preparation" && exit 1)

echo "Launching api over uvicorn ..."
uvicorn app.api:api --host 0.0.0.0 --port 8000 --reload
