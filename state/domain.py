"""
The Domain of Variables
"""


class ListDomain(object):
    def __init__(self, values):
        '''
        :param values: The list of possible values
        :type values: list of int
        '''
        self.values = values

    def possible_moves(self):
        '''
        returns an iteration of the possible values
        '''
        return iter(self.values)
