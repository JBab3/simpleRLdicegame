from random import randint
from random import uniform
import random
import numpy as np
import matplotlib.pyplot as plt


# constants that set up the RL function
HM_EPISODES = 2001
ROLL_PENALTY = 1
LOSS_PENALTY = 300
WIN_REWARD = 50
EPS_DECAY = 0.99998
HM_ROLLS = 0
SHOW_EVERY = 5000000
PRINT_FINAL_QT = True
PRINT_START_QT = False
EVALUATE = True
EVALUATE_EVERY = 100
EVALUATION_GAMES = 1000

LEARNING_RATE = 0.1
DISCOUNT = 0.9

# table that holds the Q-values and therefore decides what the player will do
q_table = {}


def main():
    epsilon = 0.9
    eval_number = 0
    winrates = []
    episode_numbers = []

    # create Qtable consisting of random Q-values. i and ii cycle through the possible rolls 1-6 on both dice.
    # iii keeps track of the number of rerolls the player has spent. The maximum possible is set by HM_ROLLS
    for i in range(0, 6):
        for ii in range(0, 6):
            for iii in range(0, HM_ROLLS+1):
                q_table[i, ii, iii] = [uniform(-5, 0) for i in range(2)]

    # print start QTable. Simple test to show the difference before and after the RL has taken place
    if PRINT_START_QT:
        print('\nQ-table after initialisation:')
        for j in range(0, 6):
            print(round(q_table[j, 0, 0][0]), round(q_table[j, 0, 0][1]), '|', round(q_table[j, 1, 0][0]),
                  round(q_table[j, 1, 0][1]), '|', round(q_table[j, 2, 0][0]), round(q_table[j, 2, 0][1]), '|',
                  round(q_table[j, 3, 0][0]), round(q_table[j, 3, 0][1]), '|', round(q_table[j, 4, 0][0]),
                  round(q_table[j, 4, 0][1]), '|', round(q_table[j, 5, 0][0]), round(q_table[j, 5, 0][1]), '|')

    # start learning
    for episode in range(HM_EPISODES):
        dice1 = randint(1, 6)
        dice2 = randint(1, 6)

        for r in range(0, HM_ROLLS+1):
            # r indicates the number of rolls used by the player
            obs = (dice1 - 1, dice2 - 1, r)

            # action chosen
            if random.random() > epsilon:
                if max(q_table[obs]) == q_table[obs][0]:
                    action = 0
                else:
                    action = 1
            else:
                action = randint(0, 1)

            # action executed
            if action == 1:
                dice2 = randint(1, 6)

            # reward identified
            if r == HM_ROLLS or action == 0:
                if dice2 >= dice1:
                    reward = WIN_REWARD
                else:
                    reward = -LOSS_PENALTY
            else:
                reward = -ROLL_PENALTY

            # new Q value identified and updated
            # the future_q value is set to 0 if the player chose to stay or has reached the max. number of rolls allowed
            if r >= HM_ROLLS or action == 0:
                max_future_q = 0
            else:
                new_obs = (dice1 - 1, dice2 - 1, r+1)
                max_future_q = max(q_table[new_obs])
            current_q = q_table[obs][action]
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            q_table[obs][action] = new_q

            if action == 0:
                break               # this ends the loop, but if the player chose to stay

        epsilon *= EPS_DECAY

        # printing the Q-table every SHOW_EVERY episodes to check on the progress.
        if episode % SHOW_EVERY == 0 and episode != 0:
            print('\nQ-table status on episode number', episode, ':')
            for jj in range(0, HM_ROLLS+1):
                for j in range(0, 6):
                    print(round(q_table[j, 0, jj][0]), round(q_table[j, 0, jj][1]), '|', round(q_table[j, 1, jj][0]),
                          round(q_table[j, 1, jj][1]), '|', round(q_table[j, 2, jj][0]), round(q_table[j, 2, jj][1]),
                          '|',
                          round(q_table[j, 3, jj][0]), round(q_table[j, 3, jj][1]), '|', round(q_table[j, 4, jj][0]),
                          round(q_table[j, 4, jj][1]), '|', round(q_table[j, 5, jj][0]), round(q_table[j, 5, jj][1]),
                          '|')

        # evaluate the performance of the current Q-Table by having the player play eval. games and tracking the wins
        if EVALUATE and episode % EVALUATE_EVERY == 0:
            eval_number += 1
            wins = 0
            for i in range(EVALUATION_GAMES):
                eval_dice1 = randint(0, 5)
                eval_dice2 = randint(0, 5)
                for ii in range(0, HM_ROLLS+1):
                    if softmax(q_table[eval_dice1, eval_dice2, ii][0], q_table[eval_dice1, eval_dice2, ii][1]) \
                            <= random.uniform(0, 1):
                        eval_dice2 = randint(0, 5)
                if eval_dice2 >= eval_dice1:
                    wins += 1
            if episode % (EVALUATE_EVERY*10) == 0:
                print('Win%:', wins*100/EVALUATION_GAMES, '| Episode:', episode, '| Eval Nr.', eval_number-1,
                      '| epsilon:', epsilon)

            # save the performance in this array to plot it after training
            episode_numbers.append(episode)
            winrates.append(wins*100/EVALUATION_GAMES)
    if PRINT_FINAL_QT:
        print('\nFinal Q-table:')
        for jj in range(0, HM_ROLLS+1):
            for j in range(0, 6):
                print(round(q_table[j, 0, jj][0]), round(q_table[j, 0, jj][1]), '|', round(q_table[j, 1, jj][0]),
                      round(q_table[j, 1, jj][1]), '|', round(q_table[j, 2, jj][0]), round(q_table[j, 2, jj][1]), '|',
                      round(q_table[j, 3, jj][0]), round(q_table[j, 3, jj][1]), '|', round(q_table[j, 4, jj][0]),
                      round(q_table[j, 4, jj][1]), '|', round(q_table[j, 5, jj][0]), round(q_table[j, 5, jj][1]), '|')
            print('________')

    plt.plot(episode_numbers, winrates)
    plt.xlabel('Episode No.')
    plt.ylabel('winrate in %')
    title = 'Player winrate at ' + str(HM_EPISODES) + ' episodes, ' + str(EVALUATION_GAMES) + ' evaluation games.'
    plt.title(title)
    plt.show()


def softmax(x, y):
    oddsforstay = (np.exp(x) / (np.exp(x) + np.exp(y)))
    return oddsforstay


def get_avg_max_future_q(qtable, dice1, r):
    avg_max_future_q = 0
    for i in range(6):
        avg_max_future_q += max(qtable[dice1, i, r+1]) / 6
    return avg_max_future_q


main()
