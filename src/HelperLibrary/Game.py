from random import randint
from time import sleep
from src.HelperLibrary.StorageFunctions import StorageFunctions


class Game:
    rounds = 5

    def __init__(self, player_one_username, player_two_username):
        self.player_one = player_one_username
        self.player_two = player_two_username
        self.player_one_score = 0
        self.player_two_score = 0

    @staticmethod
    def roll_dice():
        roll = randint(1, 6)
        return roll

    def calculate_score(self, roll_one, roll_two, current_score):
        roll_total = roll_one + roll_two
        if roll_total % 2 == 0:
            roll_total += 10
            if roll_one == roll_two:
                print("Rolling bonus die")
                sleep(randint(1, 3))
                bonus_roll = self.roll_dice()
                print("You got", bonus_roll, "for your bonus roll :)")
                roll_total += bonus_roll
        else:
            roll_total -= 5
        current_score += roll_total
        if current_score < 0:
            current_score = 0
        return current_score

    def get_winner(self):
        while self.player_one_score == self.player_two_score:
            print("TIEBREAKER!!!")
            input("Hit enter to roll tiebreaker:")
            self.player_one_score += self.roll_dice()
            self.player_two_score += self.roll_dice()
        winner = self.player_one if self.player_one_score > self.player_two_score else self.player_two
        return winner

    def play_round(self, round_number):
        print("Round number", round_number, "starting!")
        for player_number in range(2):
            player_score = self.player_one_score if (player_number + 1) == 1 else self.player_two_score
            print("Player", str(player_number + 1), ", GO!")
            input("Hit enter to roll die")
            print("Rolling first dice-")
            sleep(randint(1, 3))
            roll_one = self.roll_dice()
            print("Rolling second dice-")
            sleep(randint(0, 2))
            roll_two = self.roll_dice()
            print("You rolled a", str(roll_one), "and", str(roll_two))
            player_score = self.calculate_score(roll_one, roll_two, player_score)
            print("Your final score after this round is", str(player_score) + "!")
            if (player_number + 1) == 1:
                self.player_one_score = player_score
            else:
                self.player_two_score = player_score

    def play(self):
        for round_number in range(self.rounds):
            self.play_round(round_number + 1)
        winner = self.get_winner()
        print(winner, "is the winner!!!!!!!!")
        self.save(winner)
        print("Thank you for playing the game")
        print("---Rolling you back to menu---")

    def save(self, winner, table_name="games", user_table_name="users"):
        player_one_id = StorageFunctions(user_table_name).retrieve(["username"], [self.player_one])[0][0]
        player_two_id = StorageFunctions(user_table_name).retrieve(["username"], [self.player_two])[0][0]
        winner = player_one_id if winner == self.player_one else player_two_id
        StorageFunctions(table_name).append(
            "(player_one_id, player_two_id, player_one_score, player_two_score, winner)",
            [player_one_id, player_two_id, self.player_one_score, self.player_two_score, winner]
        )
