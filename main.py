import math

from counter_example import CounterExample
from online_covering_problem import OnlineCoveringProblem


def Test(k):
    example = CounterExample(k)
    problem = OnlineCoveringProblem(k, example.n, example.c)
    for constraint in example.constraints:
        problem.AddConstraint(constraint['a'], constraint['b'], constraint['suggestions'])
    problem.FinalizeTheVariables()

    print('The objective value:', problem.objective_value)
    print('3x the potential:', 3 * example.CalculateThePotential(problem.x))



### main ###

Test(3)
Test(9)
Test(27)
