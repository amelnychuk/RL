
import numpy as np

class Env:

    LENGTH = 3

    def __init__(self):
        self._board = np.zeros(self.LENGTH**2)
        self._index = np.arange(self.LENGTH**2)+1
        self.x = 1
        self.o = -1
        self.winner = None
        self.ended = False
        self.numStates = 3**(self.LENGTH**2)


    def reward(self, symbol):

        if not self.game_over():
            return 0

        return 1 if self.winner == symbol else 0


    def game_over(self):

        def end(player):
            self.winner = player
            self.ended = True
            return True



        board = self._board.reshape((self.LENGTH, self.LENGTH))

        for player in (self.x, self.o):
            for i in range(self.LENGTH):
                #check rows
                if board[i].sum() == player * self.LENGTH:
                    return end(player)
                #check column
                if board[:, i].sum() == player * self.LENGTH:
                    return end(player)

            #check diagonals
            if board.trace() == player * self.LENGTH:
                return end(player)

            if np.fliplr(board).trace() == player * self.LENGTH:
                return end(player)

        #check for draw
        if np.all((self._board == 0) == False):
            self.winner = None
            self.ended = True
            return True

        #game is not over
        self.ended = False
        return False


