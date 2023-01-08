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
db.users.insert(
  {
    "name": "xabi",
    "email": "xabi@xabi.com",
    "dni": "12345678",
    "password_hash" : "7791aab6b05036537893253f84f6c649f09b9d051649a8d22d545a52b66496a3",
    "password_salt" : "gimmesomepepper"
  }
)
EOF