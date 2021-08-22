from src.User.User import User


class RegisterMenuItem:
    def __init__(self):
        pass

    def execute(self):
        user = self._get_new_user_details()

    @staticmethod
    def _get_new_user_details():
        username = input("Please enter a username:").capitalize()
        password = input("Please enter a password for your account:")
        return User(username, password)

    @staticmethod
    def exit_initiated():
        return False


class LoginMenuItem:
    def __init__(self):
        pass

    @staticmethod
    def execute():
        print("Login(WIP)")

    @staticmethod
    def exit_initiated():
        return False


class InformationMenuItem:
    def __init__(self):
        pass

    @staticmethod
    def execute():
        print("No information available")

    @staticmethod
    def exit_initiated():
        return False


class ExitMenuItem:
    def __init__(self):
        self.is_exit_initiated = False

    def execute(self):
        print("Exiting...")
        self.is_exit_initiated = True

    def exit_initiated(self):
        return self.is_exit_initiated


class CLI:
    def __init__(self):
        self.main_menu_dict = {
            'r': RegisterMenuItem(),
            'l': LoginMenuItem(),
            'i': InformationMenuItem(),
            'e': ExitMenuItem(),
        }

    def initiate(self):
        print("Welcome to The OCR NEA Task Dice Game!")
        exit_initiated = False
        while not exit_initiated:
            choice = input("Enter r to register, l to login or i to get more information.\nEnter e to exit the game:").lower()
            menu_item = self.main_menu_dict.get(choice)
            if menu_item is None:
                print("Enter valid choice")
                continue
            menu_item.execute()
            exit_initiated = menu_item.exit_initiated()
