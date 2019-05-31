#!/usr/bin/env bash

eval $(docker-machine env $EC2_INSTANCE_NAME)
docker-machine ls
eval $(docker-machine env -u)
