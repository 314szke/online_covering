import math
import sys

from counter_example import CounterExample
from new_counter_example import NewCounterExample
from online_covering_problem import OnlineCoveringProblem


def Test(k):
    example = NewCounterExample(k)
    problem = OnlineCoveringProblem(k, example.n, example.c)
    for constraint in example.constraints:
        problem.AddConstraint(constraint['a'], constraint['b'], constraint['suggestions'])

    print(f'Test({k})')
    print('3x the potential before scaling:', 3 * example.CalculateThePotential(problem.x))
    problem.FinalizeTheVariables()
    print('The objective value:', problem.objective_value)
    print('3x the potential after scaling:', 3 * example.CalculateThePotential(problem.x))
    print('6x the potential after scaling:', 6 * example.CalculateThePotential(problem.x))



### main ###

Test(4)
