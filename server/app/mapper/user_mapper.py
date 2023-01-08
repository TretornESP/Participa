from app.model.user_model import UserModel

class UserMapper:
    def __init__(self):
        pass

    @staticmethod
    def repository_to_model(user):
        return UserModel(user['name'], user['email'], user['dni'], user['password_hash'], user['password_salt'])

    @staticmethod
    def model_to_repository(user):
        return {
            'name': user.get_name(),
            'email': user.get_email(),
            'dni': user.get_dni(),
            'password_hash': user.get_password_hash(),
            'password_salt': user.get_password_salt()
        }

    @staticmethod
    def repository_to_model_list(users):
        return [UserMapper.repository_to_model(user) for user in users]

    @staticmethod
    def model_to_repository_list(users):
        return [UserMapper.model_to_repository(user) for user in users]

    @staticmethod
    def model_to_dict_list(users):
        return [user.to_dict() for user in users]

    @staticmethod
    def repository_to_dict_list(users):
        return [UserMapper.repository_to_model(user).to_dict() for user in users]