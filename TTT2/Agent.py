import re
import numpy as np

class Agent:

    def __init__(self, alpha = .5, eps = .1):
        self.eps = eps
        self.alpha = alpha
        self.state_history = []
        self.V = []
        self.verbose = False

    def setSymbol(self, sym):
        """

        :param sym: (sign)
            sets the symbol of the agent.

        """
        self.symbol = sym

    def setV(self, v):
        """

        :param v: (list)
            sets the value array to be indexed by state

        :return:
        """
        #this is the learning data
        self.V = v

    def take_action(self, env):
        r = np.random.rand()
        next_move = None
        best_value = -1
        if r < self.eps:
            #take a random action
            if self.verbose:
                print "Taking random action"
            empty = env.getEmpty()
            idx = np.random.choice(empty)

            #env.getEmpty().pop(idx)
            next_move = idx
        else:
            if self.verbose:
                print "Taking greedy action"
            empty = env.getEmpty()

            for i in empty:
                #
                env.setBoard(i, self.symbol)
                value = self.V[env.getHash()]
                env.setBoard(i, 0)
                if value > best_value:
                    best_value = value
                    next_move = i

        env.setBoard(next_move, self.symbol)



    def reset_history(self):
        self.state_history = []

    def update_state_history(self, state):
        self.state_history.append(state)

    def update(self, env):
        reward = env.reward(self.symbol)
        target = reward
        for prev in reversed(self.state_history):
            value = self.V[prev] + self.alpha*(target - self.V[prev])
            self.V[prev] = value
            target = value
        self.reset_history()


class Human:

    def __init__(self):
        pass

    def set_symbol(self, symbol):
        self.symbol = symbol

    def take_action(self, env):
        pattern = re.compile("[0-2],[0-2]")
        while True:
            valid = False
            while not valid:
                move = raw_input("Enter coord row,col (i,j = 0..2)")
                if re.match(pattern, move):
                    valid = True
            i, j = move.split(',')
            i = int(i)
            j = int(j)
            idx = np.arange(9).reshape(3,3)[i,j]
            if idx in env.getEmpty():
                env.setBoard(idx, self.symbol)
                break

    def update(self, env):
        pass

    def update_state_history(self, state):
        pass





