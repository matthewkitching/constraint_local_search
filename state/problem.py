"""
The problem domain, which consists of a set of variables
and constraints
"""

from state.variables import Variable
from collections import defaultdict


class Problem(object):
    def __init__(self, variables=[], constraints=[]):
        '''
        The problem consists of a set of variables and constraints
        and a total_score, which is the sum of all the constraints
        moves_necessary states.

        :param variables: variables for the problem
        :type variables: list of state.variables.Variable
        :param constraints: constraints of the problem:
        :type constraints: list of constraints.base_constraints
        '''
        self.variables = variables
        self.variables_by_id = {
            v.identifier: v for v in variables
        }
        self.constraints = {
            c.identifier: c for c in constraints
        }

        self.variable_constraints = defaultdict(list)
        for constraint in constraints:
            for variable in constraint.variables:
                self.variable_constraints[variable.identifier].append(
                    constraint
                )
        self.total_score = sum([c.moves_necessary for c in constraints])
