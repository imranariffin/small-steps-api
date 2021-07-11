#!/bin/bash

python ./scripts/create_db.py
alembic --config ./alembic.ini upgrade head
