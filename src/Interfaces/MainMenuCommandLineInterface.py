from src.User.User import User
from src.User.Login import Login
from src.User.Registration import Registration
from src.HelperLibrary.Validator import Validator
from src.HelperLibrary.Singleton import Singleton
from src.Interfaces.GameMenuCommandLineInterface import CLI as GameCLI


class RegisterMenuItem:
    def __init__(self):
        pass

    def execute(self):
        if Validator("register").should_continue():
            user = self._get_new_user_details()
            message = Registration().register(user)
            print(message)

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
        if Validator("login").should_continue():
            logged_in = False
            try_again = True
            logged_in_usernames = []
            while (logged_in is False) and (try_again is True):
                username = input("Enter your username:").capitalize()
                password = input("Enter your password:")
                login_result = Login().login(User(username, password))
                if not login_result:
                    print("Incorrect username and/or password")
                    invalid_input = True
                    while invalid_input:
                        try:
                            try_again = bool(int(input("Would you like to try again? Enter 1 to try again and 0 to exit.")))
                        except ValueError:
                            print("Please enter either 0 or 1")
                        else:
                            invalid_input = False
                else:
                    if len(logged_in_usernames) == 1:
                        print("Both players successfully logged in!")
                        logged_in = True
                        try_again = False
                    else:
                        print("Player 1 successfully logged in!")
                    logged_in_usernames.append(username)
            if len(logged_in_usernames) == 2:
                singleton = Singleton(*logged_in_usernames)
                GameCLI(singleton).initiate()
                Singleton.reset()

    @staticmethod
    def exit_initiated():
        return False


class InformationMenuItem:
    def __init__(self):
        pass

    @staticmethod
    def execute():
        print("The OCR NEA Task Dice Game is a game developed for the GCSE NEA task.\n"
              "Github: https://github.com/mriduldhall/Dice-Game-NEA-Console")

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
