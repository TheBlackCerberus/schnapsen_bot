from api import State
import random

'''
util.get_rank(index) and util.get_suit(index) 
gets rank and suit from card number

util.get_card_name(index)
returns the rank and the suit of the card as a tuple


'''


class Bot:

    def __init__(self):
        pass
    
    #get if trump exchange 
    def trump_exchange(self, state):
        pass
    
    #return a list of marriages
    def marriage(self, state):
        moves = state.moves()
        marriages = []
        for (first, second) in moves:
            if first is not None and second is not None:
                marriages.append(first, second)
        return marriages
    
    #returns whether a move
    #TODO
    def trump_moves(self, move):
        trump_moves = []
        return trump_moves

    def get_move(self, state):
        moves = state.moves()
        trump_moves = [] 
        
        
        return random.choice(moves)