from random import randint
from random import uniform
import random


# constants that set up the RL function
HM_EPISODES = 5000
ROLL_PENALTY = 1
LOSS_PENALTY = 300
WIN_REWARD = 30
EPS_DECAY = 0.9998
SHOW_EVERY = 2501
HM_REROLLS = 1

LEARNING_RATE = 0.1
DISCOUNT = 0.95

# table that holds the Q-values and therefore decides what the 2nd player will do
q_table = {}


def main():
    epsilon = 0.9

    # create Qtable consisting of random Q-values. i indicates the number player 1 rolled.ii the number player 2 rolled.
    # iii keeps track of the number of rerolls player 2 has spent. The maximum possible is set by HM_REROLLS
    for i in range(0, 6):
        for ii in range(0, 6):
            for iii in range(0, HM_REROLLS+1):
                q_table[i, ii, iii] = [uniform(-5, 0) for i in range(2)]

    # print start QTable. Simple test to show the difference before and after the RL has taken place
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

        for rr in range(0, HM_REROLLS):
            uprr = rr                           # save the number of rerolls use as uprr
            obs = (dice1 - 1, dice2 - 1, uprr)

            # action chosen
            if random.random() > epsilon:
                if max(q_table[obs]) == q_table[obs][0]:
                    action = 0
                else:
                    action = 1
            else:
                action = randint(0, 1)
            if action == 0:
                rr = HM_REROLLS+1               # this ends the loop, but still allows for the action to be executed

            # action executed
            if action == 1:
                uprr += 1
                dice2 = randint(1, 6)

            # reward identified
            if rr == HM_REROLLS+1:
                if dice1 > dice2:
                    reward = -LOSS_PENALTY
                else:
                    reward = WIN_REWARD
            else:
                reward = -ROLL_PENALTY

            # new Q value identified and updated
            # uprr is used to change the correct Q value since rr may have been changed in order to end the loop early
            new_obs = (dice1-1, dice2-1, uprr)
            max_future_q = max(q_table[new_obs])
            current_q = q_table[obs][action]
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            q_table[obs][action] = new_q

        epsilon *= EPS_DECAY

        if episode % SHOW_EVERY == 0 and episode != 0:
            print('\nQ-table status on episode number', episode, ':')
            for jj in range(0, HM_REROLLS):
                for j in range(0, 6):
                    print(round(q_table[j, 0, jj][0]), round(q_table[j, 0, jj][1]), '|', round(q_table[j, 1, jj][0]),
                          round(q_table[j, 1, jj][1]), '|', round(q_table[j, 2, jj][0]), round(q_table[j, 2, jj][1]),
                          '|',
                          round(q_table[j, 3, jj][0]), round(q_table[j, 3, jj][1]), '|', round(q_table[j, 4, jj][0]),
                          round(q_table[j, 4, jj][1]), '|', round(q_table[j, 5, jj][0]), round(q_table[j, 5, jj][1]),
                          '|')

    print('\nFinal Q-table:')
    for jj in range(0, HM_REROLLS):
        for j in range(0, 6):
            print(round(q_table[j, 0, jj][0]), round(q_table[j, 0, jj][1]), '|', round(q_table[j, 1, jj][0]),
                  round(q_table[j, 1, jj][1]), '|', round(q_table[j, 2, jj][0]), round(q_table[j, 2, jj][1]), '|',
                  round(q_table[j, 3, jj][0]), round(q_table[j, 3, jj][1]), '|', round(q_table[j, 4, jj][0]),
                  round(q_table[j, 4, jj][1]), '|', round(q_table[j, 5, jj][0]), round(q_table[j, 5, jj][1]), '|')
        print('________')


main()
