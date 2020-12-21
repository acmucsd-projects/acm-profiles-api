#!/usr/bin/env bash

TEMP=$(echo $DATABASE_URL | cut -c12-)
export DOCKER_DB_USER=$(echo $TEMP | cut -d':' -f 1)
export DOCKER_DB_PASSWORD=$(echo $TEMP | cut -d':' -f 2 | cut -d'@' -f 1)
export DOCKER_DB_PORT=$(echo $TEMP | cut -d':' -f 3 | cut -d'/' -f 1)
export DOCKER_DB_NAME=$(echo $TEMP | cut -d':' -f 3 | cut -d'/' -f 2)