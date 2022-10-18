
# family of problems where 3 x InitialPotential < ALGO objective value
# k >= 3
class CounterExample:
    # k: number of experts
    # n: number of variables
    # m: number of constraints
    # c: costs of the variables in the objective function
    # b: right hand side of the constraints
    def __init__(self, k):
        self.k = k
        self.n = k**2
        self.m = self.n
        self.c = [1 for _ in range(n)] # uniform cost all ci = 1
        self.b = 1
        self.constraints = []

        # k-1 experts decide to set the variable with the smallest index in the constraint to 1
        # 1 expert decides to set each variable in the constraint evenly
        for j in range(m):
            new_constraint = {
                'a': [], # constraint coefficients
                'suggestions': []
            }
            for i in range(n):
                # with each new constraint we have one less variable
                if i < j: # variables which are not part of the constraint
                    new_constraint['a'].append(0)
                    new_constraint['suggestions'].append([0 for _ in range(k)])
                else:
                    new_constraint['a'].append(1) # uniform coefficients

                    if j == i: # supported decision by k-1 experts
                        suggestions_i = [1 for _ in range(k)]
                        suggestions_i[k-1] = 1/(n-j)
                        new_constraint['suggestions'].append(suggestions_i)
                    else:
                        suggestions_i = [0 for _ in range(k)]
                        suggestions_i[k-1] = 1/(n-j)
                        new_constraint['suggestions'].append(suggestions_i)

            # store the constraint
            self.constraints.append(new_constraint)


    def CalculateThePotential(self, x):
        number_of_x_smaller_than_x_dyn = 0
        for i in range(n):
            if x[i] <= (1/(n-i)):
                number_of_x_smaller_than_x_dyn += 1
        return number_of_x_smaller_than_x_dyn * math.log(self.k+1)
