from src.HelperLibrary.StorageFunctions import StorageFunctions
from src.User.User import User


class LoginStore:
    def __init__(self, table_name):
        self.table_name = table_name

    def get_user_by_username(self, username):
        user_data = StorageFunctions(self.table_name).retrieve(["username"], [username])
        if not user_data:
            return None
        else:
            user_data = user_data[0]
            return User(name=user_data[1], password=user_data[2])


class Login:
    def __init__(self, users_table_name="users"):
        self.login_store = LoginStore(users_table_name)

    def login(self, user):
        stored_user = self.login_store.get_user_by_username(user.username)
        if stored_user is None:
            return False
        elif user.password == stored_user.password:
            return True
        else:
            return False
