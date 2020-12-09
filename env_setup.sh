#STR="postgres://user:password@host:port/database_name"
TEMP=$(echo $DATABASE_URL | cut -c12-)
echo $DATABASE_URL
export DB_USER=$(echo $TEMP | cut -d':' -f 1)
echo $DB_USER
export DB_PASSWORD=$(echo $TEMP | cut -d':' -f 2 | cut -d'@' -f 1)
echo $DB_PASSWORD
export DB_HOST=$(echo $TEMP | cut -d':' -f 2 | cut -d'@' -f 2)
echo $DB_HOST
export DB_PORT=$(echo $TEMP | cut -d':' -f 3 | cut -d'/' -f 1)
echo $DB_PORT
export DB_NAME=$(echo $TEMP | cut -d':' -f 3 | cut -d'/' -f 2)
echo $DB_NAME
