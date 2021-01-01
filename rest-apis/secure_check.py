from user import User

users = [
    User(id=1, username="Joe", password="123"),
    User(id=2, username="Jane", password="secret")
]

# Dictionary comprehension
username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username: str, password: str):
    user = username_table.get(username, None)

    if user and password == user.password:
        return user


def identity(payload):
    user_id = payload["identity"]

    return userid_table.get(user_id, None)
