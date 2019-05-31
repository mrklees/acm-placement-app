#!/usr/bin/env bash

docker-machine create --driver azure --azure-subscription-id $AZURE_SUBSCRIPTION_ID --azure-resource-group $AZURE_RESOURCE_GROUP $AZURE_MACHINE_NAME
