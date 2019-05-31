#!/usr/bin/env bash

eval $(docker-machine env $AZURE_MACHINE_NAME)
docker-compose -f production.yml down
docker-compose -f production.yml up -d
eval $(docker-machine env -u)

