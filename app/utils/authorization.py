# utils/authorization.py

def check_user_role(user, required_role):
    return user.role == required_role
