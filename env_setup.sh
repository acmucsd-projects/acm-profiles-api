#STR="postgres://user:password@host:port/database_name"
TEMP=$(echo $DATABASE_URL | cut -c12-)
export DB_NAME=$(echo $TEMP | cut -d':' -f 1)
export DB_PASSWORD=$(echo $TEMP | CUT -d':' -f 2 | CUT -d'@' -f 1)
export DB_HOST=$(echo $TEMP | CUT -d':' -f 2 | CUT -d'@' -f 2)
export DB_PORT=$(echo $TEMP | CUT -d':' -f 3 | CUT -d'/' -f 1)
export DB_NAME=$(echo $TEMP | CUT -d':' -f 3 | CUT -d'/' -f 2)
