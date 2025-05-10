from app import auth
from exceptions import InvalidUsernameOrPasswordException
from security.users.model import get_by_username

@auth.verify_password
def verify_password(username, password):
    print(username, password)
    user = get_by_username(username)

    if user.password != password:
        raise InvalidUsernameOrPasswordException()

    return user
