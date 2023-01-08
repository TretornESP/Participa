class UserModel:
    def __init__(self, name, email, dni, password_hash, password_salt):
        self.name = name
        self.email = email
        self.dni = dni
        self.password_hash = password_hash
        self.password_salt = password_salt
    
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