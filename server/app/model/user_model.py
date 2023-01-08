class UserModel:
    def __init__(self, name, email, dni, password_hash, password_salt):
        self.name = name
        self.email = email
        self.dni = dni
        self.password_hash = password_hash
        self.password_salt = password_salt

    @staticmethod
    def from_dict(source):
        user = UserModel(source['name'], source['email'], source['dni'], source['password_hash'], source['password_salt'])
        return user
    
    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_dni(self):
        return self.dni

    def get_password_hash(self):
        return self.password_hash

    def get_password_salt(self):
        return self.password_salt

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'dni': self.dni,
            'password_hash': self.password_hash,
            'password_salt': self.password_salt
        }

    def to_vo_dict(self):
        data = self.to_dict()
        data.pop('password_hash')
        data.pop('password_salt')
        return data