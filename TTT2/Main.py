

import numpy as np

from Environment import Env
from Agent import Agent, Human
import time

def play_game(p1,p2,env, draw=False):

    # game loop
    player = None
    while not env.game_over():

        #play nice, play fair

        if player == p1:
            player = p2
        else:
            player = p1


        # draw board

        # make move>
        if draw:
            env.draw()
        player.take_action(env)
        # update state history
        p1.update_state_history(env.getHash())
        p2.update_state_history(env.getHash())

        # update value function
    p1.update(env)
    p2.update(env)

    # Initialize Agents



def main():

    pass
    #Init
    print "Initializing Agents"
    time.sleep(.2)
    p1 = Agent()
    p2 = Agent()
    #agents

    print "Initializing Environment..."
    time.sleep(.2)
    #environment
    e = Env()


    #Intialize Values
    print "Initializing Symbols..."
    time.sleep(.2)
    p1.setSymbol(e.x)
    p2.setSymbol(e.o)
    e.draw()
    print "Setting p1 values..."
    p1.setV(e.initValues(p1.symbol))
    V = np.where(np.copy(p1.V))
    print V
    print "Setting p2 values...."
    p2.setV(e.initValues(p2.symbol))


    #Train
    print "Begin training"
    for i in range(10000):
        print "epoch: {}".format(i)
        play_game(p1, p2, Env())
    print "Training Complete"


    #Play human as player 1
    human = Human()
    human.set_symbol(e.x)

    while True:
        play_game(p2, human, Env(), draw = True)

        answer = raw_input("Pay again? [y,n] :")
        if answer and answer.lower()[0] == 'n':
            break


if __name__ == '__main__':
    main()