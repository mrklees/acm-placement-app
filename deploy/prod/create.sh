#!/usr/bin/env bash

docker-machine create --driver amazonec2 --amazonec2-security-group $EC2_SECURITY_GROUP --amazonec2-instance-type $EC2_INSTANCE_TYPE $EC2_INSTANCE_NAME
