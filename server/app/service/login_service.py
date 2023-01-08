class LoginService:
    def __init__(self):
        pass

    @staticmethod
    def login(credentials):
        user = credentials.get_user()
        password = credentials.get_password()

        return 