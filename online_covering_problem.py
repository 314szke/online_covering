import math


class OnlineCoveringProblem:
    # k: number of experts
    # n: number of variables in the objective function
    # c: costs of the variables in the objective function
    def __init__(self, k, n, c):
        self.k = k
        self.n = n
        self.limit = 1 / 2 # used during the algorithm

        self.objective_value = 0.0
        self.x = [0.0 for _ in range(n)] # variables
        self.dx = [0.0 for _ in range(n)] # derivatives
        self.c = c # costs

        self.m = 0 # number of constraints
        self.a = [] # constraint coefficients


    # the algorithm expects the constraints in the form Sum aij xi >= 1
    # a: the coefficients of the current constraint
    # b: the right hand side of the current constraint
    def _ScaleCoefficients(self, a, b):
        if b == 1: return a
        for i in range(self.n):
            a[i] = a[i] / b
        return a


    # important to check to avoid infinite loops
    # a: the coefficients of the current constraint
    def _InvalidConstraint(self, a):
        positive_coefficients = 0
        for i in range(self.n):
            if a[i] > 0:
                positive_coefficients += a[i]
        if positive_coefficients < 1: return True
        return False


    # helper function to compute the element wise multiplication of two lists of length n
    # l1: the first list of size n
    # l2: the second list of size n
    def _MultiplyLists(self, l1, l2):
        sum_value = 0
        for i in range(self.n):
            sum_value += l1[i] * l2[i]
        return sum_value


    # calculate the derivative of each xi
    # a: the coefficients of the current constraint
    # suggestions: a matrix of size n x k with k suggestions for each variable i in [n]
    def _CalculateDerivatives(self, a, suggestions):
        for i in range(self.n):
            avg_suggestion = sum(suggestions[i]) * (1 / self.k)
            self.dx[i] = (a[i] / self.c[i]) * (self.x[i] + avg_suggestion)


    # scale the derivatives to not violate the constraint Sum aij xi <= 1/2
    # scale_ratio: available increase in the constraint / sum of derivatives
    def _ScaleDerivatives(self, scale_ratio):
        for i in range(self.n):
            self.dx[i] = scale_ratio * self.dx[i]


    # use the algorithm to satisfy the constraint which is in the form Sum aij xi >= 1
    # a: the coefficients of the current constraint
    # suggestions: a matrix of size n x k with k suggestions for each variable i in [n]
    def _SatisfyConstraint(self, a, suggestions):
        while round(self._MultiplyLists(a, self.x), 8) < round(self.limit, 8):
            self._CalculateDerivatives(a, suggestions)
            # sum the derivatives to know the expected increase in the constraint satisfaction
            sum_derivatives = sum(self.dx)

            # Sum aij xi <= 1/2 must be satisfied
            available_increase = self.limit - self._MultiplyLists(a, self.x)
            if available_increase < sum_derivatives:
                scale_ratio = available_increase / sum_derivatives
                self._ScaleDerivatives(scale_ratio)

            # increase the variables with the derivative
            for i in range(self.n):
                self.x[i] += self.dx[i]


    def AddConstraint(self, a, b, suggestions):
        # scale and check the validity of the constraint
        if len(a) < self.n: return False
        a = self._ScaleCoefficients(a, b)
        if self._InvalidConstraint(a): return False

        # store the arriving constraint in the class
        self.m += 1
        self.a.append(a)

        # use the algorithm to satisfy the constraint which is in the form Sum aij xi >= 1
        self._SatisfyConstraint(a, suggestions)
        return True


    # all xi needs to be multiplied by 2 because of the algorithm's 1/2 limit
    def FinalizeTheVariables(self):
        self.x = [x * 2 for x in self.x]
        self.objective_value = self._MultiplyLists(self.c, self.x)
