# init.sh
set -e

mongosh <<EOF
use ${MONGO_INITDB_DATABASE}
db.createUser({
  user: '$MONGODB_USER',
  pwd:  '$MONGODB_PASSWORD',
  roles: [{
    role: 'readWrite',
    db: '$MONGODB_DB'
  }]
})
EOF