import math


# family of problems where 3 x InitialPotential < ALGO objective value
# where the potential considers the xi variables of the algorithm before scaling
# k >= 4
class NewCounterExample:
    # k: number of experts
    # n: number of variables
    # m: number of constraints
    # c: costs of the variables in the objective function
    def __init__(self, k):
        self.k = k
        self.n = k**2
        self.m = self.n
        self.c = [1 for _ in range(self.n)] # uniform cost, all ci = 1
        self.constraints = []

        # k-1 experts decide to set the variable with the smallest index in the constraint to 1
        # 1 expert decides to set special_coefficient for the first two and remainder_coefficient for the third variable with the smallest index
        self.special_coefficient = 0.4
        self.remainder_coefficient = 0.2
        for j in range(self.m):
            new_constraint = {
                'a': [], # constraint coefficients
                'b': 1, # right hand side of the constraints
                'suggestions': []
            }
            for i in range(self.n):
                # with each new constraint we have one less variable
                if i < j: # variables which are not part of the constraint
                    new_constraint['a'].append(0)
                    new_constraint['suggestions'].append([0 for _ in range(self.k)])
                else:
                    new_constraint['a'].append(1) # uniform coefficients

                    if j == (self.m - 1): # last constraint
                        new_constraint['suggestions'].append([1 for _ in range(self.k)])
                    elif j == (self.m - 2): # one before the last constraint
                        if j == i: # supported decision by k-1 experts
                            suggestions_i = [1 for _ in range(self.k)]
                            suggestions_i[self.k-1] = self.special_coefficient
                            new_constraint['suggestions'].append(suggestions_i)
                        elif (j+1) == i: # supported decision by 1 expert
                            suggestions_i = [0 for _ in range(self.k)]
                            suggestions_i[self.k-1] = self.special_coefficient + self.remainder_coefficient
                            new_constraint['suggestions'].append(suggestions_i)
                        else:
                            suggestions_i = [0 for _ in range(self.k)]
                            new_constraint['suggestions'].append(suggestions_i)
                    else:
                        if j == i: # supported decision by k-1 experts
                            suggestions_i = [1 for _ in range(self.k)]
                            suggestions_i[self.k-1] = self.special_coefficient
                            new_constraint['suggestions'].append(suggestions_i)
                        elif (j+1) == i: # supported decision by 1 expert
                            suggestions_i = [0 for _ in range(self.k)]
                            suggestions_i[self.k-1] = self.special_coefficient
                            new_constraint['suggestions'].append(suggestions_i)
                        elif (j+2) == i: # supported decision by 1 expert
                            suggestions_i = [0 for _ in range(self.k)]
                            suggestions_i[self.k-1] = self.remainder_coefficient
                            new_constraint['suggestions'].append(suggestions_i)
                        else:
                            suggestions_i = [0 for _ in range(self.k)]
                            new_constraint['suggestions'].append(suggestions_i)

            # store the constraint
            self.constraints.append(new_constraint)


    def CalculateThePotential(self, x):
        number_of_x_smaller_than_x_dyn = 1
        for i in range(self.n):
            if x[i] <= self.special_coefficient:
                number_of_x_smaller_than_x_dyn += 1
        return number_of_x_smaller_than_x_dyn * math.log(self.k+1)
