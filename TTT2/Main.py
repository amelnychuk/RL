

import numpy as np

from Environment import Env
from Agent import Agent

def play_game(p1,p2,env):

    # game loop
    while not env.game_over():

        #play nice, play fair
        player = None
        if player is None:
            player = p1
        elif player is p1:
            player = p2
        elif player is p2:
            player = p1


        # draw board
        env.draw()

        # make move>
        player.take_action()
        env.draw()
        # update state history
        player.update_state_history(env.getHash())

        # update value function
        player.update(env)

    # Initialize Agents



def main():

    pass
    #Init
    p1 = Agent()
    p2 = Agent()
    #agents

    #environment
    e = Env()
    e.draw()

    #Intialize Values
    p1.setSymbol = e.x
    p2.setSymbol = e.o

    p1.setV(e.initValues(p1.symbol))
    p2.setV(e.initValues(p2.symbol))


    #Train



    #Play

if __name__ == '__main__':
    main()