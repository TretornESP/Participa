class UserModel:
    def __init__(self, uid, name, email, photo, dni, password_hash, password_salt, verified, ispublic, created_at, deleted_at, liked_proposals):
        self.uid = uid
        self.name = name
        self.email = email
        self.dni = dni
        self.photo = photo
        self.password_hash = password_hash
        self.password_salt = password_salt
        self.verified = verified
        self.ispublic = ispublic
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.liked_proposals = liked_proposals

    @staticmethod
    def from_dict(source):
        if source is None:
            return None
        user = UserModel(
            str(source['_id']),
            source['name'],
            source['email'],
            source['photo'],
            source['dni'],
            source['password_hash'],
            source['password_salt'],
            source['verified'],
            source['ispublic'],
            source['created_at'],
            source['deleted_at'],
            source['liked_proposals']
        )

        return user

    def get_uid(self):
        return self.uid
    
    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_dni(self):
        return self.dni

    def get_photo(self):
        return self.photo

    def get_password_hash(self):
        return self.password_hash

    def get_password_salt(self):
        return self.password_salt

    def get_verified(self):
        return self.verified

    def get_ispublic(self):
        return self.ispublic

    def get_created_at(self):
        return self.created_at

    def get_deleted_at(self):
        return self.deleted_at

    def get_liked_proposals(self):
        return self.liked_proposals

    def to_dict(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'email': self.email,
            'dni': self.dni,
            'photo': self.photo,
            'password_hash': self.password_hash,
            'password_salt': self.password_salt,
            'verified': self.verified,
            'ispublic': self.ispublic,
            'created_at': self.created_at,
            'deleted_at': self.deleted_at,
            'liked_proposals': self.liked_proposals
        }

    def to_creation_dict(self):
        data = self.to_dict()
        data.pop('uid')
        return data

    def to_vo_dict(self):
        data = self.to_dict()
        data.pop('password_hash')
        data.pop('password_salt')
        data.pop('dni')
        data.pop('verified')
        data.pop('created_at')
        data.pop('deleted_at')
        return data

    def to_external_vo_dict(self):
        if self.ispublic:
            data = self.to_vo_dict()
            data.pop('email')
            data.pop('liked_proposals')
            data.pop('ispublic')
            return data
        else:
            return {
                'uid': self.uid,
                'name': 'Usuario Anónimo',
                'photo': "https://participasalvaterra.es/photos/anonimo.png",
            }