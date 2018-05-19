
import numpy as np

LENGTH = 3

class Agent:


    def __init__(self, eps=0.1, alpha=0.5):
        self.eps = eps
        self.alpha = alpha
        self.verbose = False
        self.state_history = []

    def setV(self, V):
        self.V = V

    def set_symbol(self, symbol):
        self.sym = symbol

    def set_verbose(self, v):
        self.verbose = v

    def reset_history(self):
        self.state_history = []

    def take_action(self, env):
        #epsilon-greedy
        r = np.random.rand()
        best_state = None
        if r < self.eps:
            #take random action
            if self.verbose:
                print "Taking random action"

            possible_moves = []
            for i in xrange(LENGTH):
                for j in xrange(LENGTH):
                    if env.is_empty(i,j):
                        possible_moves.append((i, j))
            idx = np.random.choice(len(possible_moves))
            next_move = possible_moves[idx]
        else:
            pos2value = {}
            #greedy part
            next_move = None
            best_value = -1
            for i in xrange(LENGTH):
                for j in xrange(LENGTH):
                    if env.is_empty(i,j):
                        env.board[i,j] = self.sym
                        state = env.get_state()
                        env.board[i, j] = 0
                        pos2value[(i,j)] = self.V[state]
                        if self.V[state] > best_value:
                            best_value = self.V[state]
                            best_state = state
                            next_move = (i,j)
            if self.verbose:
                print"Taking a greedy action"
                for i in range(LENGTH):
                    print"------------------"
                    for j in range(LENGTH):
                        if env.is_empty(i, j):
                            # print the value
                            print " %.2f|" % pos2value[(i, j)]
                        else:
                            print("  ")
                            if env.board[i, j] == env.x:
                                print "x  |",
                            elif env.board[i, j] == env.o:
                                print"o  |",
                            else:
                                print"   |",
                    print ""
                print "------------------"
        env.board[next_move[0], next_move[1]] = self.sym




    def update_state_history(self, state):
        self.state_history.append(state)

    def update(self, env):
        reward = env.reward(self.sym)
        target = reward
        for prev in reversed(self.state_history):
            value = self.V[prev] + self.alpha*(target - self.V[prev])
            self.V[prev] = value
            target = value
        self.reset_history()


class Human:

    def __init__(self):
        pass

    def set_symbol(self, sym):
        self.sym = sym

    def take_action(self, env):
        while True:
            move = raw_input("Enter coord row,col (i,j = 0..2)")
            i, j = move.split(',')
            i = int(i)
            j = int(j)
            if env.is_empty(i,j):
                env.board[i,j] = self.sym
                break

    def update(self, env):
        pass

    def update_state_history(self, s):
        pass
