#!/usr/bin/env bash

eval $(docker-machine env $AZURE_MACHINE_NAME)
docker-compose -f production.yml build
eval $(docker-machine env -u)
