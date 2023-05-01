import hashlib
import secrets

class CryptographyUtil:
    def __init__(self):
        pass

    @staticmethod
    def encrypt(password, salt):
        return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

    @staticmethod
    def generate_salt():
        return str(secrets.randbits(16))

    @staticmethod
    def generate_image_key():
        return str(secrets.randbits(64))