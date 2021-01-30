# A simple reinforcement learning dice-game
A very simple reinforcement learning program designed to show that I applied the RL-algorithm to my own environment correctly 
and to find out how well reinforcementlearning handles stochastic outcomes when it comes to making decisions and awarding rewards.

## The 'game'
The game works as follows: a dice is cast showing a random number 1-6. The player then casts a second dice and after seeing both numbers can decide to reroll or stay. 
The goal for the player is to roll a higher number than the first one. If the numbers are tied the player wins.

A reinforcement learning program should be able to figure out that rerolling is the right decision when the players number is lower than the one on the first dice
and that not rerolling is correct when the player is allready winning.


## Stochastic outcomes in Qlearning

Most enviorments in which Qlearning is applied are strictly deterministic, meaning each action has one guaranteed outcome. Since this program involes the decision to reroll a dice the outcome is not guaranteed. 

The Qlearning algorithm however relies on knowing the Qvalues of future actions when evaluating how good an action is. Since the outcome of each action is random the algorithm needs to be adjusted. 
If the unchanged algorithm is apllied to this enviorment the Qvalue will be calculated based on the assumption that the player can pick what number is rolled. This of course is false.

In order to adress this the max_future_q variable is changed based not on the maximum Q value of the best future game state, but instead of the averge Q value of all possible states. This is done through the function called 'get_avg_max_future_q'.


## Evaluating the Players performance

In order to test wether or not the algorithm is improving the players performance needs to be tracked. This is done through tracking the winrate. Below is a graph showing the winrate of the player over the first 1000 episodes of training:

![1k Eps](docs/1kEps100kGames.png)
