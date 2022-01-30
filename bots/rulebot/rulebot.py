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
    __max_depth = -1
    __randomize = True

    def __init__(self, randomize=True, depth=8):
        self.__randomize = randomize
        self.__max_depth = depth

    def value(self, state, alpha=float('-inf'), beta=float('inf'), depth = 0):
        """
        Return the value of this state and the associated move
        :param State state:
        :param float alpha: The highest score that the maximizing player can guarantee given current knowledge
        :param float beta: The lowest score that the minimizing player can guarantee given current knowledge
        :param int depth: How deep we are in the tree
        :return val, move: the value of the state, and the best move.
        """

        if state.finished():
            winner, points = state.winner()
            return (points, None) if winner == 1 else (-points, None)

        if depth == self.__max_depth:
            return self.heuristic(state)

        best_value = float('-inf') if self.maximizing(state) else float('inf')
        best_move = None

        moves = state.moves()

        if self.__randomize:
            random.shuffle(moves)

        for move in moves:

            next_state = state.next(move)
            value, _ = self.value(next_state)

            if self.maximizing(state):
                if value > best_value:
                    best_value = value
                    best_move = move
                    alpha = best_value
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                    beta = best_value

            # Prune the search tree
            # We know this state will never be chosen, so we stop evaluating its children
            if beta <= alpha:
                break

        return best_value, best_move

    def maximizing(self, state):
        # type: (State) -> bool
        """
        Whether we're the maximizing player (1) or the minimizing player (2).

        :param state:
        :return:
        """
        return state.whose_turn() == 1

    def heuristic(self, state):
        # type: (State) -> float
        """
        Estimate the value of this state: -1.0 is a certain win for player 2, 1.0 is a certain win for player 1

        :param state:
        :return: A heuristic evaluation for the given state (between -1.0 and 1.0)
        """
        return util.ratio_points(state, 1) * 2.0 - 1.0, None

    #get if trump exchange 
    def trump_exchange(self, moves):
        for move in moves:
            if move[0] == None:
                return move
    
    #return a marriage play if there is one
    def get_marriages(self, moves):
        marriages = []
        for move in moves:
            if move[0] is not None and move[1] is not None:
                marriages.append(move)
        return marriages


    #returns whether a  card is low or high value
    def is_low_card(self, card_index):
        if card_index != 0 and card_index != 1:
            return True
        else:
            return False



    #returns all low value moves
    #trump: whether we want only the trump, #non-trump moves, or everything: "all" "yes" "no"
    #all = gets every low value move
    #yes = gets ONLY the trump low value move
    #no = gets ONLY the non-trump
    def low_value_moves(self, state, moves, trump="all"):
        low_value_moves = []
        if trump == "all":
            for move in moves:
                if move[0] is not None and (move[0] % 5 != 0 and move[0] % 5 != 1):
                    low_value_moves.append(move)
            return low_value_moves
        elif trump == "yes":
            for move in moves:
                if move[0] is not None and (move[0] % 5 != 0 and move[0] % 5 != 1) and state.is_trump_move(move):
                    low_value_moves.append(move)
            return low_value_moves
        elif trump == "no":
            for move in moves:
                if move[0] is not None and (move[0] % 5 != 0 and move[0] % 5 != 1) and not state.is_trump_move(move):
                    low_value_moves.append(move)
            return low_value_moves
        #if we return here, we return an empty list, we have to handle that later!
        return low_value_moves
            #if we return here, we return an empty list, we have to handle that later!
            #return low_value_moves

        
    #index % 5 == 0 or index % 5 == 1
    #moves = state.moves()
    def high_value_moves(self, state, moves, trump="all"):
        high_value_moves = []
        if trump == "all":
            for move in moves:
                if move[0] is not None and (move[0] % 5 == 0 or move[0] % 5 == 1):
                    high_value_moves.append(move)
            return high_value_moves
        elif trump == "yes":
            for move in moves:
                if move[0] is not None and (move[0] % 5 == 0 or move[0] % 5 == 1) and state.is_trump_move(move):
                    high_value_moves.append(move)
            return high_value_moves
        elif trump == "no":
            for move in moves:
                if move[0] is not None and (move[0] % 5 == 0 or move[0] % 5 == 1) and not state.is_trump_move(move):
                    high_value_moves.append(move)
            return high_value_moves
        #returns all high value moves, check low_value_moves() for documentation
        #if we return here, we return an empty list, we have to handle that later

    def is_not_empty(self, list_of_moves):
        if len(list_of_moves) != 0:
            return True
        else:
            return False

    def get_move(self, state):
        moves = state.moves()
        me = state.whose_turn()
        
        #phase 1
        if state.get_phase() == 1:
            #check if our turn
            if state.whose_turn() == me:

                for move in moves:
                    #trump exchange available play the move
                    if move[0] is None:
                        return move
                    #elif marriage_move available play the move
                    elif self.is_not_empty(self.get_marriages(moves)):
                        return self.get_marriages(moves)[0]
                    elif self.is_not_empty(self.low_value_moves(state, moves, trump="no")):
                        return self.low_value_moves(state, moves, trump="no")[0]
                    #play the lowest trump (low value moves)
                    elif self.is_not_empty(self.low_value_moves(state, moves, trump="all")):
                        return self.low_value_moves(state, moves, trump="all")[0]
                    else:
                        #play the lowest non_trump_move (high value moves)
                        if self.is_not_empty(self.high_value_moves(state, moves, trump="no")):
                            return self.high_value_moves(state, moves, trump="no")[0]
                        #play the lowest trump (high_value_moves)
                        else:
                            return self.high_value_moves(state, moves, trump="all")[0]

            else:
                # if opponent card == low:
                opponents_card = state.get_opponents_played_card()
                if self.is_low_card(opponents_card):

                    # if card is low card and trump
                    if util.get_suit(opponents_card) == state.get_trump_suit():
                        #play the lowest non_trump_move (low value moves)
                        if self.is_not_empty(self.low_value_moves(state, moves, trump="no")):
                            return self.low_value_moves(state, moves, trump="no")[0]
                            #play the lowest non_trump_move (high value moves)
                        elif self.is_not_empty(self.high_value_moves(state, moves, trump="no")):
                            return self.high_value_moves(state, moves, trump="no")[0]
                        else:
                            #play the lowest trump (low value moves)
                            if self.is_not_empty(self.low_value_moves(state, moves, trump="all")):
                                return self.low_value_moves(state, moves, trump="all")[0]
                            #play the lowest trump (high_value_moves)
                            else:
                                return self.high_value_moves(state, moves, trump="all")[0]


                    # if card is low and is not trump
                    else:
                        # if there is bigger low_value_card with same suit play that
                        if self.is_not_empty(self.low_value_moves(state, moves, trump="no")):
                            for move in self.low_value_moves(state, moves, trump="no"):
                                if util.get_suit(move[0]) == util.get_suit(opponents_card) and move[0] % 5 < opponents_card % 5:
                                    return move

                        # if there is bigger high_value_card with same suit play that
                        elif self.is_not_empty(self.high_value_moves(state, moves, trump="no")):
                            for move in self.high_value_moves(state, moves, trump="no"):
                                if util.get_suit(move[0]) == util.get_suit(opponents_card) and move[0] % 5 < opponents_card % 5:
                                    return move

                        elif self.is_not_empty(self.low_value_moves(state, moves, trump="no")):
                            return self.low_value_moves(state, moves, trump="no")[0]

                            #play the lowest non_trump_move (high value moves)
                        elif self.is_not_empty(self.high_value_moves(state, moves, trump="no")):
                            return self.high_value_moves(state, moves, trump="no")[0]

                        else:
                            #play the lowest trump (low value moves)
                            if self.is_not_empty(self.low_value_moves(state, moves, trump="all")):
                                return self.low_value_moves(state, moves, trump="all")[0]

                            #play the lowest trump (high_value_moves)
                            else:
                                return self.high_value_moves(state, moves, trump="all")[0]

                # else its high card:
                else:
                    # if card is card and trump
                    if util.get_suit(opponents_card) == state.get_trump_suit():

                        # if there is bigger trump card play that
                        if self.is_not_empty(state.get_trump_moves()):
                            for move in  state.get_trump_moves():
                                if move[0] is not None and move[0] % 5 < opponents_card % 5:
                                    return move

                        #play the lowest non_trump_move (low value moves)
                        elif self.is_not_empty(self.low_value_moves(state, moves, trump="no")):
                            return self.low_value_moves(state, moves, trump="no")[0]

                        #play the lowest non_trump_move (high value moves)
                        elif self.is_not_empty(self.high_value_moves(state, moves, trump="no")):
                            return self.high_value_moves(state, moves, trump="no")[0]
                        else:
                            ##play lowest trump card

                            #play the lowest trump (low value moves)
                            if self.is_not_empty(self.low_value_moves(state, moves, trump="all")):
                                return self.low_value_moves(state, moves, trump="all")[0]
                            #play the lowest trump (high_value_moves)
                            else:
                                return self.high_value_moves(state, moves, trump="all")[0]


                    # if it's not trump card
                    else:
                        # if there is bigger high card with same suit play that
                        if self.is_not_empty(self.high_value_moves(state, moves, trump="no")):
                            for move in self.high_value_moves(state, moves, trump="no"):
                                if util.get_suit(move[0]) == util.get_suit(opponents_card) and move[0] % 5 < opponents_card % 5:
                                    return move

                        # elif the lowest trump available
                        elif self.is_not_empty(state.get_trump_moves()):
                            return state.get_trump_moves()[0]

                        else:
                            for move in moves:
                                return move




            #######################################################################################

            #what card did he play - high v card - is it a t card - do we have a low v card
            # if state.get_opponents_played_card() is not None: #its true if a card got played by the opponent
            #     high_value_move=False
            #     for move in self.high_value_moves(self, state, moves, trump="all"):
            #         if (state.get_opponents_played_card()==move):
            #             high_value_move=True
            #     if (high_value_move==True):
            #         if (state.get_trump_suit() == util.get_suit(state.get_opponents_played_card())):
            #             pass
            #         else: #not a t card
            #             for move in moves:
            #                 for cards in self.low_value_moves(self, state, moves, trump="all"):
            #                     if move==cards:
            #                         return move
            #     else:
            #         #low v card
            #         if (state.get_trump_suit() == util.get_suit(state.get_opponents_played_card())):
            #             pass
            #
            #
            # else:
            #     #check for trump exchange play
            #
            #     #check for marriage play
            #     marriage, marriage_move = self.marriage(moves)
            #     if marriage:
            #         return marriage_move
            #     #if state.get_opponents_played_card()

        ###############################################################################################################

        #phase 2
        else:
            val, move = self.value(state)

            return move


#%%
