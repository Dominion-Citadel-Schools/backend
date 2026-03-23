
def get_user_full_name(user):
    if not user:
        return None

    full_name = f"{user.first_name} {user.last_name}".strip()

    if not full_name:
        return user.username

    return full_name.title()