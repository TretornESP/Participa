import hashlib

class CryptographyUtil:
    def __init__(self):
        pass

    @staticmethod
    def encrypt(password, salt):
        return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()