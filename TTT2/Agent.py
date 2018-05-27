
import numpy as np

class Agent:

    def __init__(self, alpha = .5, eps = .1):
        self.eps = eps
        self.alpha = alpha
        self.state_history = []
        self.V = []
        self.verbose = False

    def setSymbol(self, sym):
        self.symbol = sym

    def setV(self, v):
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
                idx = np.random.choice(env.getEmpty())
                env.getEmpty().pop(idx)
                next_move = idx
        else:

            for i in env.getEmpty():
                #
                env.setBoard(i, self.symbol)
                value = self.V[env.getHash()]
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



