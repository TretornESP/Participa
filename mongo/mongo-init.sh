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

db.users.insertMany([
  {
    "name": "xabi",
    "email": "xabi@xabi.com",
    "dni": 123123,
    "photo": "https://tretornesp.com/cuak.jpg",
    "password_hash" : "7791aab6b05036537893253f84f6c649f09b9d051649a8d22d545a52b66496a3",
    "password_salt" : "gimmesomepepper",
    "created_at": 1682974904,
    "deleted_at": 0,
    "verified": true,
    "public": true,
    "liked_proposals": []
  },
  {
    "name": "xabi2",
    "email": "xabi2@xabi.com",
    "dni": 123123,
    "photo": "https://tretornesp.com/cuak.jpg",
    "password_hash" : "7791aab6b05036537893253f84f6c649f09b9d051649a8d22d545a52b66496a3",
    "password_salt" : "gimmesomepepper",
    "verified": true,
    "created_at": 1682974904,
    "deleted_at": 0,
    "public": false,
    "liked_proposals": []
  }
])

var xabi = db.users.findOne({email: "xabi@xabi.com"})
var xabi2 = db.users.findOne({email: "xabi2@xabi.com"})

#The author of the first proposal is xabi
db.proposals.insertMany([
  {
    "title": "Arboles en la plaza",
    "description": "Me encantaria tener arboles en la plaza, son super bonitos y dan sombra",
    "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "main_photo": "https://tretornesp.com/cuak.jpg",
    "author": xabi._id,
    "created_at": 1673198346,
    "deleted_at": 0,
    "coordinates": {
      "lat": 42.08744884607051,
      "lng": -8.503972515463829
    },
    "likes": 123
  },
  {
    "title": "Gimnasio",
    "description": "Querria un gimnasio en la plaza, para poder hacer deporte",
    "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "main_photo": "https://tretornesp.com/cuak.jpg",
    "author": xabi._id,
    "created_at": 1673199346,
    "deleted_at": 0,
    "coordinates": {
      "lat": 42.08982673620478,
      "lng": -8.506367392838001
    },
    "likes": 111
  },
  {
    "title": "Rebeldia",
    "description": "Queremos abrir una delegación de rebeldía en la plaza, junto a la plaza de abastos",
    "photos": [
      "https://tretornesp.com/cuak.jpg",
      "https://tretornesp.com/cuak2.jpg"
    ],
    "main_photo": "https://tretornesp.com/cuak.jpg",
    "author": xabi2._id,
    "created_at": 1673158346,
    "deleted_at": 0,
    "coordinates": {
      "lat": 42.079786840543754,
      "lng": -8.501386530697346
    },
    "likes": 12
  }
])
EOF