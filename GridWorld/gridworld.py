

import numpy as np

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

        assert(self.current_state() in self.all_states())

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
