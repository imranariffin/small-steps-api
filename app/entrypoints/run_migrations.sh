#!/bin/bash

python ./app/create_db.py
alembic --config ./app/alembic.ini upgrade head
