#!/bin/bash

work_dir=$(pwd)

if test -f .env; then
  source .env

  if [ -n "$DEBUG" ]; then
    cp "$work_dir"/.env "$work_dir"/docker/.env

    docker_file="${work_dir}/docker/docker-compose."
    container_name="app_"

    if [[ "$DEBUG" == "True" ]]; then
      docker_file+="debug.yml"
      container_name+="debug"
    else
      docker_file+="prod.yml"
      container_name+="production"
    fi

    docker-compose -f "$docker_file" build
    docker-compose -p "$container_name" -f "$docker_file" up
  else
    echo "Can't read DEBUG from .env"
  fi
else
  echo "There's no .env file"
fi
