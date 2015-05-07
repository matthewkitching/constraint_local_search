from state.domain import ListDomain
from state.variables import Variable

def test_possible_moves():
    domain = ListDomain([0, 1, 2, 3])
    variable = Variable('id1', domain, 1)
    possible_moves = list(variable.possible_moves())
    assert([0,2,3] == possible_moves)

def test_make_move():
    domain = ListDomain([0, 1, 2, 3])
    variable = Variable('id1', domain, 1)
    variable.make_move(2)
    possible_moves = list(variable.possible_moves())
    assert([0,1,3] == possible_moves)
                
