

import numpy as np

from Environment import Env
from Agent import Agent, Human
import time

def play_game(p1,p2,env, draw=False):

    """

    The crucible....

    :param p1: (TTT2.Agent.Agent/Human)
        Player one
    :param p2: (TTT2.Agent.Agent/Human)
        Player two
    :param env: (TTT2.Env)
        Game environment
    :param draw:
        verbose argument
    :return:
    """

    # game loop
    player = None
    while not env.game_over():

        #play nice, play fair

        if player == p1:
            player = p2
        else:
            player = p1

        # make move>
        player.take_action(env)
        if draw:
            env.draw()

        if env.ended:
            env.draw()

        # update state history
        p1.update_state_history(env.getHash())
        p2.update_state_history(env.getHash())

        # update value function
    p1.update(env)
    p2.update(env)

    # Initialize Agents



def main():

    p1 = Agent()
    p2 = Agent()

    e = Env()

    p1.setSymbol(e.x)
    p2.setSymbol(e.o)

    p1.setV(e.initValues(p1.symbol))
    p2.setV(e.initValues(p2.symbol))

    for i in range(10000):
        if i % 1000 == 0:
            print "epoch: {}".format(i)
        play_game(p1, p2, Env())
    print "Training Complete"


    human = Human()
    human.set_symbol(e.o)
    p1.verbose = True

    while True:
        play_game(p1, human, Env(), draw = True)

        answer = raw_input("Pay again? [y,n] :")
        if answer and answer.lower()[0] == 'n':
            break


if __name__ == '__main__':
    main()