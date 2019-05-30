#!/usr/bin/env bash

eval $(docker-machine env $EC2_INSTANCE_NAME)
docker-compose -f production.yml up --build -d
eval $(docker-machine env -u)

