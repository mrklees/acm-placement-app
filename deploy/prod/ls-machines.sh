#!/usr/bin/env bash

eval $(docker-machine env $AZURE_MACHINE_NAME)
docker-machine ls
eval $(docker-machine env -u)
