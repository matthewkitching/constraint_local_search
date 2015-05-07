"""
This module implements constraint based local search algorithm

LocalSearch class implements a very basic local search
which performs moves by getting the variable move that
improves the problems best solution the most

make_moves is the entry point that makes a series of
moves until either a solution is reached, or a max number
of iterations is done
"""
from state.variables import Variable
from state.domain import ListDomain
from operator import attrgetter


class LocalSearch(object):
    def __init__(self, _problem):
        '''
        :param _problem: A problem instance
        :type _problem: class state.problem.Problem
        '''
        self.problem = _problem
        self.disallowed_moves = {}
        self._update_best_move_variables(self.problem.variables)

    def _move(self, variable=None, move=None):
        constraints = self.problem.variable_constraints
        if variable is None:
            variable, move = self._best_move()

        variables_to_update = set([variable])
        for constraint in constraints[variable.identifier]:
            constraint.make_move(variable, move)
            variables_to_update.update(constraint.variables)
        self.problem.total_score += variable.best_move_delta_score
        variable.state = move
        self._update_best_move_variables(variables_to_update)

    def _best_move(self):
        var = min(
            self.problem.variables,
            key=attrgetter('best_move_delta_score')
        )
        return var, var.best_move_value

    def _update_best_move_variables(self, variables_to_update):
        constraints = self.problem.variable_constraints
        for variable in variables_to_update:
            variable.best_move_delta_score = float("inf")
            for value in variable.possible_moves():
                total_delta = 0
                for constraint in constraints[variable.identifier]:
                    total_delta += constraint.get_delta_moves_necessary(
                        variable, value
                    )
                if total_delta < variable.best_move_delta_score:
                    variable.best_move_delta_score = total_delta
                    variable.best_move_value = value

    def make_moves(self, max_iterations):
        '''
        performs moves until we reach the max number of iterations
        :param max_iterations: The max number of iterations before exit
        :type max_iterations: int
        '''
        for index in range(max_iterations):
            self._move()
            if self.problem.total_score == 0:
                return
