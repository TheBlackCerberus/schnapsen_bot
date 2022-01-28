from api import State, util
import random



'''
|          | Aces | 10s | Kings | Queens | Jacks |
|:--------:|:----:|:---:|:-----:|:------:|:-----:|
|   Clubs  |   0  |  1  |   2   |    3   |   4   |
|  Diamonds|   5  |  6  |   7   |    8   |   9   |
|  Hearts  |  10  |  11 |   12  |   13   |   14  |
|  Spades  |  15  |  16 |   17  |   18   |   19  |
'''


'''
util.get_rank(index) and util.get_suit(index) 
gets rank and suit from card number

util.get_card_name(index)
returns the rank and the suit of the card as a tuple

trump_suit = state.get_trump_suit()

state.__phase returns the phase number: 1 or 2 as an intiger

returns whose turn it is, player 1 or 2
self.leader():

_deck.can_exchange(self, player):

state.get_trump_moves(self):

state.get_opponents_played_card() returns the index of the card
'''

class Bot:
    def __init__(self):
        pass

    #get if trump exchange 
    def trump_exchange(self, moves):
        for move in moves:
            if move[0] == None:
                return move
    
    #return a marriage play if there is one
    def marriage(self, moves):
        marriages = []
        for (first, second) in moves:
            if first is not None and second is not None:
                marriage = True
                move = (first, second)
                return marriage, move
        
        return False, (None, None)
    
    #returns a sorted list of tuples (cards) by value
    #its in descending order (first highest, last lowest value)
    def sort_cards(self,cards):
        sorted(cards, key=lambda card_index: card_index[0]%5)

    #returns whether a  card is low or high value
    def card_value(self, state, move):
        pass
        #maybe not needed

    #returns all low value moves
    #trump: whether we want only the trump, #non-trump moves, or everything: "all" "yes" "no"
    #all = gets every low value move
    #yes = gets ONLY the trump low value move
    #no = gets ONLY the non-trump
    def low_value_moves(self, state, moves, trump="all"): 
        low_value_moves = []
        if trump == "all":
            for move in moves:
                if move[0] % 5 != 0 and move[0] % 5 != 1:
                    low_value_moves.append(move)
            return low_value_moves        
        elif trump == "yes":
            for move in moves:
                if move[0] % 5 != 0 and move[0] % 5 != 1 and state.get_trump_suit() == util.get_suit(move[0]):
                    low_value_moves.append(move)
            return self.sort_cards(low_value_moves)
        elif trump == "no":
            for move in moves:
                if move[0] % 5 != 0 and move[0] % 5 != 1 and state.get_trump_suit() != util.get_suit(move[0]):
                    low_value_moves.append(move)
            return self.sort_cards(low_value_moves)
        
        #if we return here, we return an empty list, we have to handle that later!
        return low_value_moves


        
    #index % 5 == 0 or index % 5 == 1
    #moves = state.moves()

    #returns all high value moves, check low_value_moves() for documentation
    def high_value_moves(self, state, moves, trump="all"):
        high_value_moves = []
        if trump == "all":
            for move in moves:
                if move[0] % 5 == 0 or move[0] % 5 == 1:
                    high_value_moves.append(move)
            return self.sort_cards(high_value_moves)
        elif trump == "yes":
            for move in moves:
                if move[0] % 5 == 0 or move[0] % 5 == 1 and state.get_trump_suit() == util.get_suit(move[0]):
                    high_value_moves.append(move)
            return self.sort_cards(high_value_moves)
        elif trump == "no":
            #state.get_trump_suit() == util.get_suit(index) 
            for move in moves:
                if move[0] % 5 == 0 or move[0] % 5 == 1 and state.get_trump_suit() != util.get_suit(move[0]):
                    high_value_moves.append(move)
            
            return self.sort_cards(high_value_moves)

        #if we return here, we return an empty list, we have to handle that later!
        return high_value_moves


    def get_move(self, state):
        moves = state.moves()
        
        #phase 1
        if state.get_phase() == 1:
            #check if opp played a card
            #what card did he play - high v card - is it a t card - do we have a low v card
            if state.get_opponents_played_card() is not None: #its true if a card got played by the opponent
                high_value_move=False
                for move in self.high_value_moves(self, state, moves, trump="all"):
                    if (state.get_opponents_played_card()==move):
                        high_value_move=True
                if (high_value_move==True):
                    if (state.get_trump_suit() == util.get_suit(state.get_opponents_played_card())):
                        pass
                    else: #not a t card
                        for move in moves:
                            for cards in self.low_value_moves(self, state, moves, trump="all"):
                                if move==cards:
                                    return move
                else: 
                    #low v card
                    if (state.get_trump_suit() == util.get_suit(state.get_opponents_played_card())):
                        pass

                    
            else: 
                #check for trump exchange play

                #check for marriage play
                marriage, marriage_move = self.marriage(moves)
                if marriage: 
                    return marriage_move
                #if state.get_opponents_played_card()

        #phase 2
        else:            
            #call alphabeta
            pass
        
        return random.choice(moves)
