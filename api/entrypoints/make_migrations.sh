#!/bin/bash

echo REVISION_NAME_SUFFIX=$REVISION_NAME_SUFFIX
[ -z "$REVISION_NAME_SUFFIX" ] \
  && echo "Must provide environment variable REVISION_NAME_SUFFIX" \
  && exit 1

python ./wait_for_db.py
alembic --config ./alembic.ini revision --autogenerate -m "$REVISION_NAME_SUFFIX"
