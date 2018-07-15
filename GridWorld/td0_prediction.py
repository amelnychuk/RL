

"""
tutorial from lazyprogrammer
"""

from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
from gridworld import standard_grid, negative_grid, ALL_POSSIBLE_ACTIONS
from iterative_policy_evaluation import print_values, print_policy

SMALL_ENOUGH = 1e-3
GAMMA = .9
ALPHA = .1

def random_action(a, eps=.1):

    p = np.random.random()
    if p < (1 -eps):
        return a
    else:
        return np.random.choice(ALL_POSSIBLE_ACTIONS)


def play_game(grid, policy):
    s = (2,0)
    grid.set_state(s)
    states_and_rewards = [(s, 0)]
    while not grid.game_over():
        a = policy[s]
        a = random_action(a)
        r = grid.move(a)
        s = grid.current_state()
        states_and_rewards.append((s,r))
    return states_and_rewards


if __name__ == '__main__':
    grid = standard_grid()
    print("rewards:")
    print_values(grid.rewards(), grid)

    policy = {
        (2, 0): 'U',
        (1, 0): 'U',
        (0, 0): 'R',
        (0, 1): 'R',
        (0, 2): 'R',
        (1, 2): 'R',
        (2, 1): 'R',
        (2, 2): 'R',
        (2, 3): 'U',
    }

    V = {}
    states = grid.all_states()
    for s in states:
        V[s] = 0

    for it in range(10000):

        states_and_rewards = play_game(grid, policy)

        for t in range(len(states_and_rewards) - 1):
            s, _ = states_and_rewards[t]
            s2, r = states_and_rewards[t+1]

            V[s] = V[s] + ALPHA*(r + GAMMA*V[s2] - V[s])

    print("values:")
    print_values(V, grid)
    print("policy:")
    print_policy(policy, grid)


