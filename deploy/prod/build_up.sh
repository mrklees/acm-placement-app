#!/usr/bin/env bash

eval $(docker-machine env $AZURE_MACHINE_NAME)
docker-compose -f production.yml up --build -d
eval $(docker-machine env -u)

