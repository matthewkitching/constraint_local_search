"""
base constraints includes a BaseConstraint object,
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
