#!/bin/bash

if [ $BUILD_ENV != "test" ];
then
  echo "Wrong BUILD_ENV=$BUILD_ENV. Must be BUILD_ENV=test"
  exit 1
fi

python ./app/create_db.py
alembic --config ./app/alembic.ini upgrade head
pytest -vvv
