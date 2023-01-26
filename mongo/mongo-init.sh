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

db.users.insertMany([
  {
    "name": "xabi",
    "email": "xabi@xabi.com",
    "dni": 4123124,
    "photo": "https://tretornesp.com/cuak.jpg",
    "password_hash" : "7791aab6b05036537893253f84f6c649f09b9d051649a8d22d545a52b66496a3",
    "password_salt" : "gimmesomepepper"
  },
  {
    "name": "xabi2",
    "email": "xabi2@xabi.com",
    "dni": 123123,
    "photo": "https://tretornesp.com/cuak.jpg",
    "password_hash" : "7791aab6b05036537893253f84f6c649f09b9d051649a8d22d545a52b66496a3",
    "password_salt" : "gimmesomepepper"
  }
])

db.proposals.insertMany([
  {
    "title": "Proposal 1",
    "description": "Proposal 1 description",
    "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "author": "xabi@xabi.com",
    "created_at": 1673198346,
    "likes": 123
  },
  {
    "title": "Proposal 2",
    "description": "Proposal 2 description",
      "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "author": "xabi@xabi.com",
    "created_at": 1673198446,
    "likes": 222
  },
    {
    "title": "Proposal 3",
    "description": "Proposal 3 description",
      "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "author": "xabi@xabi.com",
    "created_at": 1673198446,
    "likes": 222
  },
    {
    "title": "Proposal 4",
    "description": "Proposal 4 description",
      "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "author": "xabi@xabi.com",
    "created_at": 1673198446,
    "likes": 222
  },
    {
    "title": "Proposal 5",
    "description": "Proposal 5 description",
      "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "author": "xabi@xabi.com",
    "created_at": 1673198446,
    "likes": 222
  },
    {
    "title": "Proposal 6",
    "description": "Proposal 6 description",
      "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "author": "xabi@xabi.com",
    "created_at": 1673198446,
    "likes": 222
  },
    {
    "title": "Proposal 7",
    "description": "Proposal 7 description",
      "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "author": "xabi@xabi.com",
    "created_at": 1673198446,
    "likes": 222
  },
    {
    "title": "Proposal 8",
    "description": "Proposal 8 description",
      "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "author": "xabi@xabi.com",
    "created_at": 1673198446,
    "likes": 222
  },
    {
    "title": "Proposal 9",
    "description": "Proposal 9 description",
      "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "author": "xabi@xabi.com",
    "created_at": 1673198446,
    "likes": 222
  },
    {
    "title": "Proposal 10",
    "description": "Proposal 10 description",
      "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "author": "xabi@xabi.com",
    "created_at": 1673198446,
    "likes": 222
  },
    {
    "title": "Proposal 11",
    "description": "Proposal 11 description",
      "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "author": "xabi@xabi.com",
    "created_at": 1673198446,
    "likes": 222
  },
    {
    "title": "Proposal 12",
    "description": "Proposal 12 description",
      "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "author": "xabi@xabi.com",
    "created_at": 1673198446,
    "likes": 222
  },
    {
    "title": "Proposal 13",
    "description": "Proposal 13 description",
      "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "author": "xabi@xabi.com",
    "created_at": 1673198446,
    "likes": 222
  }
])
EOF