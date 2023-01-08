class CredentialsModel:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def get_user(self):
        return self.user

    def get_password(self):
        return self.password