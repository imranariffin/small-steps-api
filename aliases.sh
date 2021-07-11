#!/bin/bash

alias set_envs='export $(cat .env.$BUILD_ENV | grep -vE "(^#|^$)" | xargs)'
alias dc='docker-compose --env-file .env.${BUILD_ENV}'
alias d='docker'
alias dclear_containers='d container stop $(d container ls --all -q) && d container rm $(d container ls --all -q)'
