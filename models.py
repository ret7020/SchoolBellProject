from flask_login import UserMixin

class LoginnedUserModel(UserMixin):
    def __init__(self, fake_id):
        self.id = fake_id

    @classmethod
    def get(cls, id):
        return LoginnedUserModel(1)

