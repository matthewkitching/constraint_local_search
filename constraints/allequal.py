from constraints.base_constraint import BaseConstraint
from collections import defaultdict


class AllEqual(BaseConstraint):
    def __init__(self, variables, identifier=None):
        '''
        AllEqual Constraint is satisfied if all the variables are
        assigned the same value.
        moves_necessary is the number of moves to achieve this,
        which is equal to the number of variables - the cardinatlity
        of the most common value
        '''
        super(AllEqual, self).__init__(variables, identifier)
        self._reinit()

    def _reinit(self):
        self.score_count = defaultdict(int)
        for variable in self.variables:
            self.score_count[variable.state] += 1
        self.max_value = max(self.score_count, key=self.score_count.get)
        self.max_count = self.score_count[self.max_value]
        self.moves_necessary = len(self.variables) - self.max_count

    def get_delta_moves_necessary(self, variable, new_value):
        new_count = self.score_count[new_value] + 1
        if new_count > self.max_count:
            return -1
        if new_count == self.max_count:
            return 0
        if variable.state == self.max_value:
            return +1
        return 0

    def make_move(self, variable, new_value):
        self.score_count[variable.state] -= 1
        self.score_count[new_value] += 1
        if self.score_count[new_value] >= self.max_count:
            self.max_count = self.score_count[new_value]
            self.max_value = new_value
        elif variable.state == self.max_value:
            self.max_value = max(self.score_count, key=self.score_count.get)
            self.max_count = self.score_count[self.max_value]
        old_moves_necessary = self.moves_necessary
        self.moves_necessary = len(self.variables) - self.max_count
        return old_moves_necessary - self.moves_necessary

    def get_moves_necessary(self):
        return self.moves_necessary
