# init.sh
set -e

mongosh <<EOF
use ${MONGO_INITDB_DATABASE}

EOF