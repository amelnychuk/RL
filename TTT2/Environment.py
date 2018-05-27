
import numpy as np
from itertools import product
from tabulate import tabulate

class Env:

    LENGTH = 3

    def __init__(self):
        self._board = np.zeros(self.LENGTH**2)
        self.calcStateHash()
        self._empty = np.arange(self.LENGTH**2).tolist()

        self._state = self.calcStateHash()
        self.x = 1
        self.o = -1
        self.winner = None
        self.ended = False
        self.numStates = 3**(self.LENGTH**2)

    def getEmpty(self):
        """

        :return: (np.array)
            converts the zeros in self._board to an array of indecies
        """
        return np.where(self.getBoard() == 0)

    def setBoard(self, index, symbol):
        self._board[index] = symbol
        self.calcStateHash()

    def getBoard(self):
        return self._board

    def reward(self, symbol):

        if not self.game_over():
            return 0

        return 1 if self.winner == symbol else 0

    def victory(self, player):
        self.winner = player
        self.ended = True

    def draw(self):
        self.winner = None
        self.ended = True


    def game_over(self, force_recalculate=False):

        if not force_recalculate and self.ended:
            return self.ended

        board = self._board.reshape((self.LENGTH, self.LENGTH))

        for player in (self.x, self.o):
            for i in range(self.LENGTH):
                #check rows
                if board[i].sum() == player * self.LENGTH:
                    self.victory(player)
                #check column
                if board[:, i].sum() == player * self.LENGTH:
                    self.victory(player)

            #check diagonals
            if board.trace() == player * self.LENGTH:
                self.victory(player)

            if np.fliplr(board).trace() == player * self.LENGTH:
                self.victory(player)

        #check for draw
        if np.all((self._board == 0) == False):
            self.draw()

        #game is not over
        self.ended = False

    def permutations(self):
        """
        Generator for all the states of the game board.

        """
        for permutation in product(product([0,self.x, self.o], repeat=self.LENGTH), repeat=self.LENGTH):
            yield np.array(permutation).flatten()

    def calcStateHash(self):

        board = np.copy(self.getBoard())
        seed = board[board == -1] = 2
        indices = np.arange(self.LENGTH**2)**3

        self._hash = (seed + indices).sum()

    def getHash(self):
        return self._hash


    def initValues(self, symbol):

        #calculate state triplet for
        V = np.zeros(self.numStates())
        value = 0
        for state in self.permutations():

            self.setBoard(state)
            self.calcStateHash()
            self.game_over(force_recalculate=True)

            if self.ended == True:
                if self.winner is None:
                    value = .5

                else:

                    if self.winner == symbol:
                        value = 1
                    else:
                        value = 0


            V[self.getHash()] = value
        return V

    def draw(self):

        values = [self.x, 0, self.o]
        symbols = ['x', ' ', 'o']
        board = self.getBoard().reshape((3,3)).tolist()
        symbol_board = [[symbols[values.index(v)] for v in row] for row in board]
        print tabulate(symbol_board, tablefmt='grid')








