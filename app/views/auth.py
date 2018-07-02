from werkzeug.security import safe_str_cmp
from app.views.users import User


def authenticate(first_name, password):
    """
    :param first_name:
    :param username: The username in string format
    :param password: The un-encrypted password in string format
    :return:
    """
    user = User.find_by_username(first_name)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    """

    :param payload: A dictionary with 'identity' key which is user id
    :return:
    """
    user_id = payload['identity']
    return User.find_by_id(user_id)

