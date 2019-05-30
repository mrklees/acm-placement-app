#!/usr/bin/env bash

eval $(docker-machine env $EC2_INSTANCE_NAME)
docker-compose -f production.yml run --rm django python manage.py createsuperuser
eval $(docker-machine env -u)

