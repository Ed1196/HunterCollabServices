from werkzeug.security import safe_str_cmp


# Auth using username and password. Will be triggered by /auth
from models.users import UserModel


def authentica(email, password):
    user = UserModel.findUserByEmail(email)
    if user and safe_str_cmp(password,user.password):
        return user

# Retrieves User ID from JWT and uses that id to find that user in the DB
def identity(payload):
    user_id = payload['identity']
    return UserModel.findById(user_id)
