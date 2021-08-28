from src.HelperLibrary.Game import Game


class GameMenuItem:
    def __init__(self, singleton):
        self.player_one_username = singleton.player_one
        self.player_two_username = singleton.player_two

    def execute(self):
        Game(self.player_one_username, self.player_two_username).play()

    @staticmethod
    def exit_initiated():
        return False


class LeaderboardMenuItem:
    def __init__(self):
        pass

    @staticmethod
    def execute():
        print("Leaderboard(WIP)")

    @staticmethod
    def exit_initiated():
        return False


class LogoutMenuItem:
    def __init__(self):
        self.is_exit_initiated = False

    def execute(self):
        print("Logging out...")
        self.is_exit_initiated = True

    def exit_initiated(self):
        return self.is_exit_initiated


class CLI:
    def __init__(self, singleton):
        self.main_menu_dict = {
            'g': GameMenuItem(singleton),
            'l': LeaderboardMenuItem(),
            'e': LogoutMenuItem(),
        }

    def initiate(self):
        exit_initiated = False
        while not exit_initiated:
            choice = input("Enter g to launch game, l to view leaderboard or e to logout:").lower()
            menu_item = self.main_menu_dict.get(choice)
            if menu_item is None:
                print("Enter valid choice")
                continue
            menu_item.execute()
            exit_initiated = menu_item.exit_initiated()
