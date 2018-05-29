import re
import numpy as np
from tabulate import tabulate

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
        """

        :param env: (TTT2.Env)
            A tic tac toe environment

        Explore or exploit algorithm to determine best move.
        """

        r = np.random.rand()
        next_move = None
        best_value = -1
        values = np.zeros(env.LENGTH**2)
        if self.verbose:
            print "Computer's turn..."
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
                values[i] = value
                if value > best_value:
                    best_value = value
                    next_move = i
            if self.verbose:
                value_matrix = values.reshape(3, 3)
                print tabulate(value_matrix, tablefmt='grid')


        env.setBoard(next_move, self.symbol)



    def reset_history(self):
        """
        Clear states from history
        :return:
        """
        self.state_history = []

    def update_state_history(self, state):
        """

        Memory for the previous states

        :param state: (int)
            base 3 hash of the game board
        :return:
        """
        self.state_history.append(state)

    def update(self, env):
        """

        The RL value update function

        :param env: (TTT2.Environment.Env)

        :return:
        """
        reward = env.reward(self.symbol)
        target = reward
        for prev in reversed(self.state_history):
            value = self.V[prev] + self.alpha * (target - self.V[prev])
            self.V[prev] = value
            target = value
        self.reset_history()


class Human:
    """
    Base class to provide human input to play tic tac toe
    """


    def __init__(self):
        pass

    def set_symbol(self, symbol):
        """
        Set the symbol of the human.
        :param symbol: (sign)
            The environemt symbol
        :return:
        """
        self.symbol = symbol

    def take_action(self, env, verbose=False):
        """
        Player input
        :param env: (TTT2.Environemnt.Env)
            The game environment
        :param verbose:
            default arg to match up with the Agent.take_action arguments
        :return:
        """
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





