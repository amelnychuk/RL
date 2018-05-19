import numpy as np

LENGTH = 3

class Env(object):

    def __init__(self):
        self.board = np.zeros((LENGTH, LENGTH))
        self.x = -1
        self.o = 1
        self.winner = None
        self.ended = False
        self.num_states = 3**(LENGTH*LENGTH)

    def is_empty(self,i,j):
        return self.board[i,j] == 0

    def reward(self, symbol):

        if not self.game_over():
            return 0

        return 1 if self.winner == symbol else 0

    def get_state(self):
        """
        returns a state represented by a base 3 number
        :return:
        """

        k,h = 0
        for i in xrange(LENGTH):
            for j in xrange(LENGTH):
                if self.board[i,j] == 0:
                    v = 0
                elif self.board[i,j] == self.x:
                    v = 1
                elif self.board[i,j] == self.o:
                    v = 2
                h += (3**k) * v
                k +=1
        return h

    def set_end_var(self, player):
        self.winner = player
        self.ended = True
        return True


    def game_over(self, force_recalculate=False):

        if not force_recalculate and self.ended:
            return self.ended

        #check for draw
        if np.all((self.board == 0) == False):
            self.winner = None
            self.ended = True
            return True

        #check for win
        for player in (self.x, self.o):

            #check diagnoals
            if self.board.trace() == player*LENGTH:
                return self.set_end_var(player)

            if np.fliplr(self.board).trace() == player*LENGTH:
                return self.set_end_var(player)

            for i in xrange(LENGTH):

                #check row
                if self.board[i].sum() == player*LENGTH:
                    return self.set_end_var(player)

                #check column
                if self.board[:,i].sum() == player*LENGTH:
                    return self.set_end_var(player)

        self.winner = None
        return False


    def draw_board(self):
        for i in xrange(LENGTH):
            print "-"*10
            for j in xrange(LENGTH):
                print " ",
                if self.board[i,j] == self.x:
                    print "x",
                elif self.board[i,j] == self.o:
                    print "o",
                else:
                    print " ",
                print ""
            print "-"*10

