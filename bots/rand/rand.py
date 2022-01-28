"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State, util
import random


class Bot:

    def __init__(self):
        pass

    def marriage(self, moves):
        marriages = []
        for (first, second) in moves:
            if first is not None and second is not None:
                marriage = True
                move = (first, second)
                return marriage, move
        
        return False, (None, None)

    def sort_cards(self,cards):
        sorted(cards, key=lambda card_index: card_index[0]%5)

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
        # type: (State) -> tuple[int, int]
        """
        Function that gets called every turn. This is where to implement the strategies.
        Be sure to make a legal move. Illegal moves, like giving an index of a card you
        don't own or proposing an illegal mariage, will lose you the game.
       	TODO: add some more explanation
        :param State state: An object representing the gamestate. This includes a link to
            the states of all the cards, the trick and the points.
        :return: A tuple of integers or a tuple of an integer and None,
            indicating a move; the first indicates the card played in the trick, the second a
            potential spouse.
        """

        # All legal moves
        moves = state.moves()


        for move in moves:
            if move[0] == None:
                return move

        
        high_value_moves = self.high_value_moves(state, moves, trump="all")
        low_value_moves = self.low_value_moves(state, moves, trump="all")
        randomcar = 


        print()
        print("HIGH VALUE MOVES: ")
        
        for move in moves:
            if move[0] % 5 == 0 or move[0] % 5 == 1:
                print(move, end='')

                
        print()
        print("LOW VALUE MOVES: ")
        if(low_value_moves):
            for i in low_value_moves:
                print(i, end=' ')
        print()
        print()
      

        
        return random.choice(moves)