# Constraint Based Local Search
Implements a basic version of constraint based local search found in:
```
@book{
    VanHentenryck:2005:CLS:1121598,
    author = {Van Hentenryck, Pascal and Michel, Laurent},
    title = {Constraint-Based Local Search},
    year = {2005},
    isbn = {0262220776},
    publisher = {The MIT Press},
}
```

## High level overview
At a high level, the problem is modeled as a set of variables and a set of constraints over these variables.
### Variables
A variable has a domain of possible values, and a current state. Currently, domains are only implemented as sets of integers, and a current state as a single integer. A variable is able to move between states.
###Constraint
A constraint is defined as a relation over a set of variables. Given the set of variables and the current state of these variables, a constraint is either satisfied or unsatisfied. The violation degree is the number of moves needed to satisfy the constraint.

For example, an AllDifferent constraint is satisfied if all the variables of the constraint have different values. Suppose the six variables in the constraint have the following states:

```
AllDifferent with variables: [V1=1 V2=2 V3=2 V4=2 V5=3 V6=3]
```
Here the AllDifferent constraint is violated because V2, V3, and V4 have the same value, and V5 and V6 have the same values. The violation degree is 3, since you would have to move any two of the variables (V2, V3, and V4), and any one of the variables (V5, V6) to new values in order to satisfy the AllDifferent constraint.

A constraint maintains properties such as its satisfiability, its violation degree, and how much each of its underlying variables contribute to the violations. It can be queried to evaluate the effect of local moves on these properties.

In order for Constraint Based Local Search to be efficient, the violation degree must be incremented, rather than recalculated if the recalculation is time consuming.

## Problem
The problem is modeled as a set of variables and a set of constraints over these variables. The problem also has the total violation degree, which is the total of the violation degree of all it's constraints. When the violation degree of the problem is zero, the problem is solved.

## Moves
Currently, the only type of move implemented is a simple change of a variable state. The local search selects the move that will decreases the violation degree of the problem. In order for Local Search to be efficient, the selection of a variable must made efficiently.

# Example
The following is an example of a local search with 9 variables, each with a domain of [1,2,3,4]. There are four constraints to the problem.
```
from state.problem import Problem
from algorithms.local_search import LocalSearch

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
problem = Problem(variables, constraints)
local_search = LocalSearch(problem)
local_search.make_moves(1000)
print [(v.identifier, v.state) for v in problem.variables]
```
The output of the program is:
```
[('id0', 4), ('id1', 1), ('id2', 2), ('id3', 2), ('id4', 1), ('id5', 4), ('id6', 3), ('id7', 1), ('id8', 4)]
```
All variables are assigned a state in their domain, and all the constraints are satisfied.
