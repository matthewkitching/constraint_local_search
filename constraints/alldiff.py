from constraints.base_constraint import BaseConstraint
from collections import defaultdict


class AllDifferent(BaseConstraint):
    def __init__(self, variables, identifier=None):
        '''
        AllDifferent is satisfied if every variable is assigned a different
        value.
        The moves_necessary is equal to the total number of variables that
        have the same value as other variables ignoring one of the duplicates)
        '''
        super(AllDifferent, self).__init__(variables, identifier)
        self._reinit()

    def _reinit(self):
        self.score_count = defaultdict(int)
        for variable in self.variables:
            self.score_count[variable.state] += 1
        self.moves_necessary = len(self.variables) - len(self.score_count)

    def get_delta_moves_necessary(self, variable, new_value):
        delta_old = 0 if self.score_count[variable.state] == 1 else -1
        delta_new = 0 if self.score_count.get(new_value, 0) == 0 else 1
        return delta_new + delta_old

    def make_move(self, variable, new_value):
        self.score_count[variable.state] -= 1
        self.score_count[new_value] += 1
        delta_moves = self.get_delta_moves_necessary(variable, new_value)
        self.moves_necessary += delta_moves
        return delta_moves
