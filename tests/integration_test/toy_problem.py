from constraints.alldiff import AllDifferent
from constraints.allequal import AllEqual
from state.domain import ListDomain
from state.variables import Variable
from state.problem import Problem
from algorithms.local_search import LocalSearch


class TestLocalSearch(object):
    def __init__(self):
        variables = [
            Variable('id0', ListDomain([1, 2, 3, 4]), 1),
            Variable('id1', ListDomain([1, 2, 3, 4]), 1),
            Variable('id2', ListDomain([1, 2, 3, 4]), 1),
            Variable('id3', ListDomain([1, 2, 3, 4]), 1),
            Variable('id4', ListDomain([1, 2, 3, 4]), 1),
            Variable('id5', ListDomain([1, 2, 3, 4]), 1),
            Variable('id6', ListDomain([1, 2, 3, 4]), 1),
            Variable('id7', ListDomain([1, 2, 3, 4]), 1),
            Variable('id8', ListDomain([1, 2, 3, 4]), 1),
        ]
        constraints = [
            AllDifferent(
                [variables[0], variables[1], variables[2], variables[6]]
            ),
            AllDifferent([variables[3], variables[4], variables[5]]),
            AllEqual([variables[0], variables[5], variables[8]]),
            AllEqual([variables[1], variables[4], variables[7]]),
        ]
        self.problem = Problem(variables, constraints)

    def test_LocalSearchInit(self):
        local_search = LocalSearch(self.problem)
        for variable in self.problem.variables:
            assert(variable.best_move_value in [2, 3, 4])

        vars_by_id = self.problem.variables_by_id

        assert(vars_by_id['id0'].best_move_delta_score == 0)
        assert(vars_by_id['id1'].best_move_delta_score == 0)
        assert(vars_by_id['id2'].best_move_delta_score == -1)
        assert(vars_by_id['id3'].best_move_delta_score == -1)
        assert(vars_by_id['id4'].best_move_delta_score == 0)
        assert(vars_by_id['id5'].best_move_delta_score == 0)
        assert(vars_by_id['id6'].best_move_delta_score == -1)
        assert(vars_by_id['id7'].best_move_delta_score == 1)
        assert(vars_by_id['id8'].best_move_delta_score == 1)
        assert(self.problem.total_score == 5)

    def test_LocalSearchBestMove(self):
        local_search = LocalSearch(self.problem)
        var, val = local_search._best_move()
        assert(var.identifier in ['id2', 'id3', 'id6'])
        assert(val in [2, 3, 4])

    def test_LocalSearchMove(self):
        local_search = LocalSearch(self.problem)
        v2 = self.problem.variables_by_id['id2']
        local_search._move(variable=v2, move=2)

        vars_by_id = self.problem.variables_by_id

        assert(vars_by_id['id2'].state == 2)
        assert(vars_by_id['id0'].best_move_value in [3, 4])
        assert(vars_by_id['id1'].best_move_value in [3, 4])
        assert(vars_by_id['id2'].best_move_value in [3, 4])
        assert(vars_by_id['id3'].best_move_value in [2, 3, 4])
        assert(vars_by_id['id4'].best_move_value in [2, 3, 4])
        assert(vars_by_id['id5'].best_move_value in [2, 3, 4])
        assert(vars_by_id['id6'].best_move_value in [3, 4])
        assert(vars_by_id['id7'].best_move_value in [2, 3, 4])
        assert(vars_by_id['id8'].best_move_value in [2, 3, 4])

        assert(vars_by_id['id0'].best_move_delta_score == 0)
        assert(vars_by_id['id1'].best_move_delta_score == 0)
        assert(vars_by_id['id2'].best_move_delta_score == 0)
        assert(vars_by_id['id3'].best_move_delta_score == -1)
        assert(vars_by_id['id4'].best_move_delta_score == 0)
        assert(vars_by_id['id5'].best_move_delta_score == 0)
        assert(vars_by_id['id6'].best_move_delta_score == -1)
        assert(vars_by_id['id7'].best_move_delta_score == 1)
        assert(vars_by_id['id8'].best_move_delta_score == 1)
        assert(self.problem.total_score == 4)

    def test_Solve(self):
        local_search = LocalSearch(self.problem)
        local_search.make_moves(1000)
        assert(local_search.problem.total_score == 0)
        vars_by_id = self.problem.variables_by_id
        assert(vars_by_id['id0'].state == vars_by_id['id5'].state)
        assert(vars_by_id['id0'].state == vars_by_id['id8'].state)
        assert(vars_by_id['id1'].state == vars_by_id['id4'].state)
        assert(vars_by_id['id1'].state == vars_by_id['id7'].state)

        states = set(
            [
                vars_by_id['id0'].state,
                vars_by_id['id1'].state,
                vars_by_id['id2'].state,
                vars_by_id['id6'].state
            ]
        )
        assert(states == set([1, 2, 3, 4]))
        states = set(
            [
                vars_by_id['id3'].state,
                vars_by_id['id4'].state,
                vars_by_id['id5'].state
            ]
        )
        assert(len(states) == 3)
