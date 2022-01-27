<<<<<<< Updated upstream
"""
This is Matt's branch for rulebot (just a statement, don't actually do this)
"""
=======
from api import State
import random

# Suit order: CLUBS, DIAMONDS, HEARTS, SPADES

# 0, 5, 10, 15 - Aces
# 1, 6, 11, 16 - 10s
# 2, 7, 12, 17 - Kings
# 3, 8, 13, 18 - Queens
# 4, 9, 14, 19 - Jacks

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
        # add a card that is trump exchange
        pass
    
    #return a list of marriages
    def marriage(self, state):
        moves = state.moves()
        marriages = []
        for (first, second) in moves:
            if first is not None and second is not None:
                marriages.append(first, second)
        return marriages
    
    #returns whether a  card is low or high value
    def card_value(self, state, move):
        pass
    
    #returns all low value moves
    #trump: whether we want only the trump, #non-trump moves, or everything
    def low_value_moves(self, state, trump="all"): 
        pass
    
    #returns all high value moves
    def high_value_moves(self, state, trump="all"):
        pass    

    #returns whether a move
    def trump_moves(self, move):
        trump_moves = []
        return trump_moves

    def get_move(self, state):
        moves = state.moves()
        trump_moves = [] 
        
        
        return random.choice(moves)
>>>>>>> Stashed changes
