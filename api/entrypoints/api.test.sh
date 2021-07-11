#!/bin/bash

BUILD_ENV_EXPECTED="test"
if [ $BUILD_ENV != $BUILD_ENV_EXPECTED ];
then
  echo "Wrong BUILD_ENV=$BUILD_ENV. Must be BUILD_ENV=$BUILD_ENV_EXPECTED"
  exit 1
fi

python ./scripts/create_db.py
alembic --config ./alembic.ini upgrade head
python -m pytest -vvv
