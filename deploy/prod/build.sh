#!/usr/bin/env bash

eval $(docker-machine env $EC2_INSTANCE_NAME)
docker-compose -f production.yml build
