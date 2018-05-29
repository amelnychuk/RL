
import numpy as np
from itertools import product
from tabulate import tabulate

class Env:

    LENGTH = 3

    def __init__(self):
        self.resetBoard()
        self.calcStateHash()
        self.x = 1
        self.o = -1
        self.winner = None
        self.ended = False
        self.numStates = 3**(self.LENGTH**2)
        self.verbose = False


    def resetBoard(self):

        """
        Set's board to all zeros. Also calculates the state hash.
        :return:
        """
        self._board = np.zeros(self.LENGTH**2)
        self.calcStateHash()

    def getEmpty(self):
        """

        :return: (np.array)
            converts the zeros in self._board to an array of indecies
        """
        return np.where(self.getBoard() == 0)[0]

    def setBoard(self, index, symbol):
        '''

        :param index: (int)
            0 - (self.LENGTH**2)-1
        :param symbol: (int)
            sets the board and calculates the hash of the board
        :return:
        '''
        self._board[index] = symbol
        self.calcStateHash()

    def getBoard(self):
        '''

        :return: (np.array)
            the board is a single dim np.array
        '''
        return self._board

    def reward(self, symbol):
        """

        :param symbol: (int)
            The symbol of that one.
        :return: (bool)
            The reward for the update fn

        """

        if not self.game_over():
            return 0

        return 1 if self.winner == symbol else 0

    def victory(self, player):
        """
        Sets the environment variables for a game winner
        :param player: (int)
            the symbol of the player

        """
        if self.verbose:
            print "Victory"

        self.winner = player
        self.ended = True


    def tie(self):
        """
        Sets the environment variables incase of a tie
        :return:
        """
        if self.verbose:
            print "It is balanced, as all things should be."
        self.winner = None
        self.ended = True


    def game_over(self, force_recalculate=False):
        """
        Check for a game ending state
        :param force_recalculate: (bool)

        :return: (Bool)
            Game ended or not

        """

        if not force_recalculate and self.ended:
            return self.ended

        board = self._board.reshape((self.LENGTH, self.LENGTH))

        for player in (self.x, self.o):
            win_value = player * self.LENGTH
            for i in range(self.LENGTH):
                #check rows
                if board[i].sum() == win_value:
                    self.victory(player)
                    return True
                #check column
                if board[:, i].sum() == win_value:
                    self.victory(player)
                    return True

            #check diagonals
            if board.trace() == win_value:
                self.victory(player)
                return True

            if np.fliplr(board).trace() == win_value:
                self.victory(player)
                return True

        #check for draw
        if np.all((self._board == 0) == False):
            self.tie()
            return True

        self.winner = None
        return False




    def permutations(self):
        """
        Generator for all the states of the game board. Excessive

        """
        for permutation in product(product([0,self.x, self.o], repeat=self.LENGTH), repeat=self.LENGTH):
            yield np.array(permutation).flatten()

    def calcStateHash(self):
        """
        Calculates the hash as a base 3 number for the game board.
        :return:
        """

        board = np.copy(self.getBoard())
        board[board == -1] = 2

        indices = np.arange(self.LENGTH**2)
        base = np.ones(self.LENGTH**2)*3

        self._hash = int((np.power(base, indices) * board).sum())


    def getHash(self):
        """

        :return: (int)
            base 3 hash of the game board.
        """
        return self._hash


    def initValues(self, symbol):
        """
        Initializes the values for the agents. Loop through all the permutations to assign a value to the
        winning states.
        :param symbol: (sign)
            Agent symbol -1 or 1
        :return:
        """

        V = np.zeros(self.numStates)

        for state in self.permutations():

            self._board = state
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

        self.resetBoard()
        return V

    def draw(self):
        """
        Draws the game board. remaps the game symbol values to characters.
        :return:
        """

        values = [self.x, 0, self.o]
        symbols = ['x', ' ', 'o']
        board = self.getBoard().reshape((3, 3)).tolist()
        symbol_board = [[symbols[values.index(v)] for v in row] for row in board]
        print tabulate(symbol_board, tablefmt='grid')








