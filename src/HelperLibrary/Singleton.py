class Singleton:
    __instance = None

    @staticmethod
    def getinstance():
        if Singleton.__instance is None:
            raise Exception("Singleton does not exist!")
        return Singleton.__instance

    def __init__(self, player_one_username, player_two_username):
        if Singleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.player_one = player_one_username
            self.player_two = player_two_username
            Singleton.__instance = True

    @staticmethod
    def reset():
        Singleton.__instance = None
