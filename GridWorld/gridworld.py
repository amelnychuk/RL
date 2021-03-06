

import numpy as np

ALL_POSSIBLE_ACTIONS = ('U','D','L','R')

class Coordinate:
    def __init__(self):

        self.i = 0
        self.j = 0

class Grid:
    def __init__(self, width, height, start):
        self._width = width
        self._height = height
        self.i = start[0]
        self.j = start[1]

    def set(self, rewards, actions):
        self._rewards = rewards
        self._actions = actions

    def actions(self):
        return self._actions

    def rewards(self):
        return self._rewards

    def set_state(self, s):
        self.i = s[0]
        self.j = s[1]

    def current_state(self):
        return (self.i, self.j)

    def is_terminal(self, s):
        return s not in self._actions

    def move(self, action):
        if action in self._actions[(self.i, self.j)]:
            if action == 'U':
                self.i -= 1
            if action == 'D':
                self.i += 1
            if action == 'R':
                self.j += 1
            if action == 'L':
                self.j -= 1

        return self._rewards.get((self.i,self.j), 0)

    def undo_move(self, action):
        if action in self._actions[(self.i, self.j)]:
            if action == 'U':
                self.i += 1
            if action == 'D':
                self.i -= 1
            if action == 'R':
                self.j -= 1
            if action == 'L':
                self.j += 1

        assert(self.current_state() in self.all_states())

    def game_over(self):
        return (self.i, self.j) not in self._actions

    def all_states(self):
        return set(self._actions.keys()) | set(self._rewards.keys())

def standard_grid():

    g = Grid(3, 4, (2,0))
    rewards = {(0,3):1, (1,3): -1}
    actions = {
    (0, 0): ('D', 'R'),
    (0, 1): ('L', 'R'),
    (0, 2): ('L', 'D', 'R'),
    (1, 0): ('U', 'D'),
    (1, 2): ('U', 'D', 'R'),
    (2, 0): ('U', 'R'),
    (2, 1): ('L', 'R'),
    (2, 2): ('L', 'R', 'U'),
    (2, 3): ('L', 'U'),
  }
    g.set(rewards, actions)
    return g

def negative_grid(step_cost=.1):
    g = standard_grid()
    g._rewards.update({
        (0,0): step_cost,
        (0,1): step_cost,
        (0,2): step_cost,
        (1,0): step_cost,
        (1,2): step_cost,
        (2,0): step_cost,
        (2,1): step_cost,
        (2,2): step_cost,
        (2,3): step_cost,
    })

    return g

