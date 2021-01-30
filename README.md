# A simple reinforcement learning dice-game
A very simple reinforcement learning program designed to show that I applied the RL-algorithm to my own environment correctly
and to find out how well reinforcement learning handles stochastic outcomes when it comes to making decisions and awarding rewards.

## The rules of the game being played
The game works as follows: a dice is cast showing a random number 1-6. The player then casts a second dice and after seeing both numbers can decide to reroll or stay.
The goal for the player is to roll a higher number than the first one. If the numbers are tied the player wins.

A reinforcement learning program should be able to figure out that rerolling is the right decision when the players number is lower than the one on the first dice
and that not rerolling is correct when the player is allready winning.


## Stochastic outcomes in Q-learning

Most environments in which Q-learning is applied are strictly deterministic, meaning each action has one guaranteed outcome. Since this program involves the decision to reroll a dice the outcome is not guaranteed.

The Q-learning algorithm however relies on knowing the Q-values of future actions when evaluating how good an action is. Since the outcome of each action is random the algorithm needs to be adjusted.
If the unchanged algorithm is applied to this environment the Qvalue will be calculated based on the assumption that the player can pick what number is rolled. This of course is false.

In order to address this the max_future_q variable is changed based not on the maximum Q value of the best future game state, but instead of the average Q value of all possible states.
This should allow good decisions to backpropagate and is done through the function called 'get_avg_max_future_q'.


## Evaluating the Players performance

In order to test whether or not the algorithm is improving the players performance needs to be tracked. This is done through tracking the winrate. Below is a graph showing the winrate of the player over the first 1000 episodes of training:

![1k Eps](docs/1kEps100kGames.png)

Overall the win rate appears to be improving steadily. This is exactly what I was hoping to achieve!

There is still a lot of fluctuation both during the early training and around the 74.5% winrate mark that is the best possible avg. that is achievable. This might just be caused by the randomness inherent in a dice game, but it could also be caused by a bug.
In order to further investigate I evaluated the game for a much larger number of episodes:

![1k Eps](docs/200kEps75kGames.png)

The winrate stays near the 74.5%-mark, while still fluctuating. As this program was only designed to test whether or not RL can handle stochastic outcomes I am very happy with this outcome.
It appears that it should be possible to apply this technique to a more complex dice game, which is what had been my intention for after this project is finished.


#### Sidenote:

It is possible to change the number of rolls a player has to win. If this is used the code creates several Q-tables and trains each one separately. This is technically unnecessary as each Q-table is applied to the same situation.
One could save time and computer memory by using the same Q-table for every situation. This would also increase the rate at which the player's performance improves.

I decided not to do this here, because this program was only a test for a different dice game that I play to work on after this project is finished.
In that the player will also get several choices, however in that game several different Q-tables will be necessary as there are more different situations that require individual decision-making.

