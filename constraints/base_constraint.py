"""
base constraints includes a BaseConstraint object,
and two variations of the BaseConstraint object. TODO: move the
other two instances
"""
import operator
from collections import defaultdict
from collections import OrderedDict


class BaseConstraint(object):
    static_id_number = 0

    def __init__(self, variables, identifier):
        '''
        param variables: the variables of the constraint
        type variables: list of class state.variables.Variable
        param identifier: the identifier of the constraint
        type identifier: string or None
        '''
        self.variables = set(variables)
        if identifier is None:
            identifier = 'generated_' + str(self.static_id_number)
            self.static_id_number += 1
        self.identifier = identifier

    def get_delta_moves_necessary(self, variable, new_value):
        '''
        Gets the difference in the number of moves necessary
        to solve the constraint if variable is set to new_value
        :param variable: the variable to be moved
        :type variable: class state.variables.Variable
        :param new_value: the value to set variable
        :type new_value: int
        '''
        raise NotImplementedError

    def make_move(self, variable, new_value):
        '''
        changes the data structure based on the assignment
        variable=new_value
        :param variable: the variable to be moved
        :type variable: class state.variables.Variable
        :param new_value: the value to set variable
        :type new_value: int
        '''
        raise NotImplementedError


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
        self.reinit()

    def reinit(self):
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


class AllDifferent(BaseConstraint):
    def __init__(self, variables, identifier=None):
        '''
        AllDifferent is satisfied if every variable is assigned a different
        value.
        The moves_necessary is equal to the total number of variables that
        have the same value as other variables ignoring one of the duplicates)
        '''
        super(AllDifferent, self).__init__(variables, identifier)
        self.reinit()

    def reinit(self):
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
