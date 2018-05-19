import numpy as np

from Environment import Environment
from Agent import Agent, Human


def get_state_hash_and_winner(env, i=0, j=0):
    results = []

    for v in (0, env.x, env.o):
        env.board[i,j] = v
        if j == 2:
            if i == 2:
                state = env.get_state()
                ended = env.game_over(force_recalculate=True)
                winner = env.winner
                results.append((state, winner, ended))
            else:
                results += get_state_hash_and_winner(env, i+1, 0)
        else:
            results += get_state_hash_and_winner(env,i,j+1)

    return results

def initialV(env, symbol, state_winner_triples):
    print "Initializeing V{}".format(symbol)
    V = np.zeros(env.num_states)
    for state, winner, ended in state_winner_triples:
        if ended:
            if winner == getattr(env, symbol):
                print "winner: {}".format(winner)
                v = 1
            else:
                v = 0
        else:
            v = .5
        V[state] = v
    return V


def play_game(p1, p2, env, draw=False):
    #game loop
    current_player = None
    while not env.game_over():
        #players take turns
        if current_player == p1:
            current_player = p2
        else:
            current_player = p1

        #draw board
        if draw:
            if draw == 1 and current_player == p1:
                env.draw_board()
            if draw == 2 and current_player == p2:
                env.draw_board()

        #make a move
        current_player.take_action(env)

        #update state histories

        state = env.get_state()
        p1.update_state_history(state)
        p2.update_state_history(state)

    if draw:
        env.draw_board()

    #update value function
    p1.update(env)
    p2.update(env)


if __name__ == '__main__':

    #init
    p1 = Agent()
    p2 = Agent()

    env = Environment()
    state_winner_triples = get_state_hash_and_winner(env)

    Vx = initialV(env, 'x',state_winner_triples)
    p1.setV(Vx)
    Vo = initialV(env, 'o',state_winner_triples)
    p2.setV(Vo)

    p1.set_symbol(env.x)
    p2.set_symbol(env.o)

    #train
    T = 10000
    print "Training"
    for t in xrange(T):
        if t % 200 == 0:
            print t
        play_game(p1, p2, Environment(), draw=1)
    print "Training complete"
    #play
    human = Human()
    human.set_symbol(env.o)

    while True:
        p1.set_verbose(True)
        play_game(p1, human, Environment(), draw=2)

        answer = raw_input("Play again? [y,n]: ")
        if answer and answer.lower()[0] == 'n':
            break

