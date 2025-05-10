from exceptions import NotFoundException, InvalidUsernameOrPasswordException
from models import User

def get_by_username(username):
    user = User.query.filter_by(username=username).one_or_none()
    if user is None:
        raise InvalidUsernameOrPasswordException()

    return user