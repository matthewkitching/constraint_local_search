"""
Variable represents a variable of the problem
with a domain and a current state.
"""


class Variable(object):
    def __init__(self, identifier, domain, initial):
        '''
        :param identifier: The id of the variable
        :type identifier: string
        :param domain: The domain of the variable
        :type domain: class state.domain.ListDomain
        :param initial: The initial state of the variable
        :type initial: element of domain.possible_moves
        '''
        self.identifier = identifier
        self.domain = domain
        self.state = initial
        self.best_move_delta_score = None
        self.best_move_value = None

    def possible_moves(self):
        '''
        yields the possible moves of the domain
        which are those moves not equal to state
        '''
        for move in self.domain.possible_moves():
            if move != self.state:
                yield move

    def make_move(self, move):
        '''
        makes a move
        :param move: the move to make to the variable
        :type move: element of self.domain.possible_moves
        '''
        self.state = move
