#!/bin/bash
set -e

mongo <<EOF
use admin
db.createUser(
  {
    user: "${MONGO_USER}",
    pwd: "${MONGO_PASS}",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
  }
)

use ${MONGO_DB_NAME}
db.createCollection("users")
db.createCollection("proposals")
db.createCollection("photos")

EOF