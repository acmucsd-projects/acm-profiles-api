#!/usr/bin/env bash

TEMP=$(echo $DATABASE_URL | cut -c12-)
export DB_USER=$(echo $TEMP | cut -d':' -f 1)
export DB_PASSWORD=$(echo $TEMP | cut -d':' -f 2 | cut -d'@' -f 1)
# export DB_HOST=$(echo $TEMP | cut -d':' -f 2 | cut -d'@' -f 2)
export DB_PORT=$(echo $TEMP | cut -d':' -f 3 | cut -d'/' -f 1)
export DB_NAME=$(echo $TEMP | cut -d':' -f 3 | cut -d'/' -f 2)