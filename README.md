# Dice-Game-NEA-Console
A console solution for the GCSE OCR NEA Dice Game task

## Task
Katarina is developing a two-player dice game.

The  players  roll  two  6-sided  dice  each  and  get  points  depending  on  what  they  roll. There are 5 rounds in a game. In each round, each player rolls the two dice.

The rules are:<br/>
• The points rolled on each player’s dice are added to their score<br/>
• If the total is an even number, an additional 10 points are added to their score<br/>
• If the total is an odd number, 5 points are subtracted from their score<br/>
• If they roll a double, they get to roll one extra die and get the number of points rolled added to their score<br/>
• The score of a player cannot go below 0 at any point<br/>
• The person with the highest score at the end of the 5 rounds wins<br/>
• If  both  players  have  the  same  score  at  the  end  of  the  5  rounds,  they  each  roll  1  die  and  whoever gets the highest score wins (this repeats until someone wins).<br/>
Only authorised players are allowed to play the game. Where appropriate, input from the user should be validated.

Design, develop, test and evaluate a program that:
1. Allows  two  players  to  enter  their  details,  which  are  then  authenticated  to  ensure  that  they  are  authorised players
2. Allows each player to roll two 6-sided dice
3. Calculates and outputs the points for each round and each player’s total score
4. Allows the players to play 5 rounds
.If  both  players  have  the  same  score  after  5  rounds,  allows  each  player  to  roll  1  die  each  until  someone wins
5. Outputs who has won at the end of the 5 rounds
6. Stores the winner’s score, and their name, in an external file
7. Displays the score and player name of the top 5 winning scores from the external file

##Usage
1. Clone this repository using: https://github.com/mriduldhall/Dice-Game-NEA-Console.git
2. Open a command line session and navigate to cloned folder
3. Install requirements using: `pip install -r requirements.txt`
4. Create a file called `.env-vars` in the `src` folder and add the following while replacing everything inside `""` with your own PostgreSQL database credentials: </br>
`name="<database name>"`</br>
`user="<user>"`</br>
`password="<user password>"`</br>
`host="<database host>"`</br>
`port="<database port>"`
5. Run `setup.py` to set-up database
6. Use `python -m pytest -v` to run unit tests to ensure the game is working
7. Run `src/Main.py` to run game

##License
[MIT License](https://github.com/mriduldhall/Dice-Game-NEA-Console/blob/main/LICENSE)
