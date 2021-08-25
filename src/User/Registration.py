from src.HelperLibrary.StorageFunctions import StorageFunctions


class RegistrationStore:
    def __init__(self, table_name):
        self.table_name = table_name

    def check_if_user_exists(self, username):
        user_data = StorageFunctions(self.table_name).retrieve(["username"], [username])
        if not user_data:
            return False
        else:
            return True

    def add_user(self, user):
        StorageFunctions(self.table_name).append("(username, password)", [user.username, user.password])


class Registration:
    def __init__(self, user_table_name="users"):
        self.user_storage = RegistrationStore(user_table_name)

    def register(self, user):
        if not self.user_storage.check_if_user_exists(user.username):
            self.user_storage.add_user(user)
            return "You have successfully created an account with the username " + user.username
        else:
            return "Username is already taken"
