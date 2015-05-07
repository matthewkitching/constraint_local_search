from constraints.base_constraint import AllEqual, AllDifferent
from state.variables import Variable
from state.domain import ListDomain

class TestAllEqual(object):
    def setUp(self):
        self.variables = [
            Variable('id1', ListDomain([1,2,3,4]), 1),
            Variable('id2', ListDomain([1,2,3,4]), 2),
            Variable('id3', ListDomain([1,2,3,4]), 2),
            Variable('id4', ListDomain([1,2,3,4]), 2),
            Variable('id5', ListDomain([1,2,3,4]), 3),
            Variable('id6', ListDomain([1,2,3,4]), 3),
        ]

    def test_calculate_move_necessary(self):
        all_equal = AllEqual(self.variables)
        assert(all_equal.score_count[1] == 1)
        assert(all_equal.score_count[2] == 3)
        assert(all_equal.score_count[3] == 2)
        assert(all_equal.max_value == 2)
        assert(all_equal.max_count == 3)
        assert(all_equal.moves_necessary == 3)

    def test_get_delta_moves_into_best(self):
        all_equal = AllEqual(self.variables)
        delta = all_equal.get_delta_moves_necessary(
            self.variables[5], 2
        )
        assert(delta == -1)

    def test_get_delta_between_two_inferior(self):
        all_equal = AllEqual(self.variables)
        delta = all_equal.get_delta_moves_necessary(
            self.variables[0], 3
        )
        assert(delta == 0)

    def test_get_delta_from_best_to_almost(self):
        all_equal = AllEqual(self.variables)
        delta = all_equal.get_delta_moves_necessary(
            self.variables[1], 3
        )
        assert(delta == 0)

    def test_get_delta_from_best_to_bad(self):
        all_equal = AllEqual(self.variables)
        delta = all_equal.get_delta_moves_necessary(
            self.variables[1], 1
        )
        assert(delta == 1)
                                
        
    def test_get_delta_from_best_tied(self):
        self.variables[0].make_move(3)
        all_equal = AllEqual(self.variables)
        delta = all_equal.get_delta_moves_necessary(
            self.variables[1], 3
        )
        assert(delta == -1)
        delta = all_equal.get_delta_moves_necessary(
            self.variables[0], 2
        )
        assert(delta == -1)
                
    def test_make_move_better_move(self):
         all_equal = AllEqual(self.variables)
         all_equal.make_move(self.variables[5], 2)
         assert(all_equal.score_count[1] == 1)
         assert(all_equal.score_count[2] == 4)
         assert(all_equal.score_count[3] == 1)
         assert(all_equal.max_value == 2)
         assert(all_equal.max_count == 4)

    def test_make_tied_move_better_move(self):
        all_equal = AllEqual(self.variables)
        all_equal.make_move(self.variables[2], 4)
        assert(all_equal.score_count[1] == 1)
        assert(all_equal.score_count[2] == 2)
        assert(all_equal.score_count[3] == 2)
        assert(all_equal.score_count[4] == 1)
        assert(all_equal.max_value in [2, 3])
        assert(all_equal.max_count == 2)
        self.variables[2].state = 4
        all_equal.make_move(self.variables[2], 3)
        assert(all_equal.score_count[1] == 1)
        assert(all_equal.score_count[2] == 2)
        assert(all_equal.score_count[3] == 3)
        assert(all_equal.max_value == 3)
        assert(all_equal.max_count == 3)

    def test_move_worse(self):
        all_equal = AllEqual(self.variables)
        all_equal.make_move(self.variables[2], 3)
        assert(all_equal.score_count[1] == 1)
        assert(all_equal.score_count[2] == 2) 
        assert(all_equal.score_count[3] == 3)
        assert(all_equal.max_value == 3)
        assert(all_equal.max_count == 3)
                                                                                        

class TestAllDiff(object):
    def setUp(self):
        self.variables = [
            Variable('id1', ListDomain([1,2,3,4]), 1),
            Variable('id2', ListDomain([1,2,3,4]), 2),
            Variable('id3', ListDomain([1,2,3,4]), 2),
            Variable('id4', ListDomain([1,2,3,4]), 2),
            Variable('id5', ListDomain([1,2,3,4]), 3),
            Variable('id6', ListDomain([1,2,3,4]), 3),
        ]

    def test_calculate_move_necessary(self):
        all_diff = AllDifferent(self.variables)
        assert(all_diff.score_count[1] == 1)
        assert(all_diff.score_count[2] == 3)
        assert(all_diff.score_count[3] == 2)
        assert(all_diff.moves_necessary == 3)

    def test_delta_from_multiple_to_new(self):
        all_diff = AllDifferent(self.variables)
        delta = all_diff.get_delta_moves_necessary(self.variables[1], 4)  
        assert(delta == -1)

    def test_delta_from_multiple_to_multiple(self):
        all_diff = AllDifferent(self.variables)
        delta = all_diff.get_delta_moves_necessary(self.variables[1], 3)
        assert(delta == 0)

    def test_delta_from_multiple_to_single(self):
        all_diff = AllDifferent(self.variables)
        delta = all_diff.get_delta_moves_necessary(self.variables[1], 1)
        assert(delta == 0)

    def test_delta_from_single_to_multiple(self):
        all_diff = AllDifferent(self.variables)
        delta = all_diff.get_delta_moves_necessary(self.variables[0], 2)
        assert(delta == 1)

    def test_delta_from_single_to_new(self):
        all_diff = AllDifferent(self.variables)
        delta = all_diff.get_delta_moves_necessary(self.variables[0], 4)
        assert(delta == 0)

    def test_move(self):
        all_diff = AllDifferent(self.variables)
        delta = all_diff.make_move(self.variables[0], 2)
        assert(all_diff.score_count[1] == 0)
        assert(all_diff.score_count[2] == 4)
