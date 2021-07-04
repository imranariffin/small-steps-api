#!/bin/bash

export $(grep -v '# ' .env.test | grep -v -e '^$' | xargs)
pytest -vvv
