

from gridworld import standard_grid
import numpy as np


SMALL_ENOUGH = 1e-3

def print_values():
    pass

def print_policy():
    pass

def main():
    grid = standard_grid()

    states = grid.all_states()

    V = {}
    for s in states:
        V[s] = 0
    gamma = 1.0

    while True:
        biggest_change = 0
        for s in states:
            old_v = V[s]

            if s in grid.actions:
                new_v = 0
                p_a = 1.0 / len(grid.actions[s])
                for a in grid.actions:
                    grid.set_state(s)
                    r = grid.move(a)
                    new_v += p_a * (r + gamma * V[grid.current_state()])
                V[s] = new_v
                biggest_change = max(biggest_change, np.abs(old_v - V[s]))
            if biggest_change < SMALL_ENOUGH:
                break
    #continue to impliment thursday


if __name__ == '__main__':
    main()