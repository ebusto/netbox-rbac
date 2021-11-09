from .. import auth


class Driver:
    def __init__(self, config):
        self.config = config

    def session(self):
        return Session(**self.config)


class Session:
    def __init__(self, users):
        self.users  = users
        self.groups = []

    def authenticate(self, username, password):
        user = filter(
            lambda u: u["username"] == username and u["password"] == password,
            self.users,
        )

        user = next(user, None)

        if not user:
            raise Exception("invalid credentials")

        self.groups = user["groups"]

        return auth.Account(
            email      = user["email"],
            first_name = user["first_name"],
            last_name  = user["last_name"],
        )

    def close(self):
        pass

    def member(self, username, groups):
        for group in groups:
            if group in self.groups:
                return True

        return False
