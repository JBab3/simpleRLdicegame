# simpleRLdicegame
A very simple reinforcement learning program designed to show that I applied the RL-algorithm to my own environment correctly 
and to find out how well reinforcementlearning handles stochastic outcomes when awarding rewards.

## The 'game'
The game works as follows: a dice is cast showing a random number 1-6. The player then casts a dice too and after seeing both numbers can decide to reroll or stay. 
The goal for the player is to have a higher number than the first one. If it is a tie the player wins.

A reinforcement learning program should be able to figure out that rerolling is the right decision when the players number is lower than the first number 
and that not rerolling is correct when the player is allready winning.
