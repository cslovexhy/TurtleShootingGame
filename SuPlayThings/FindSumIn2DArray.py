from copy import deepcopy

matrix = [
    [1, 2, 3],
    [3, 4, 5]
]

class Solver:
    def __init__(self, matrix):
        assert(matrix and matrix[0])
        m, n = len(matrix), len(matrix[0])
        self.dp = deepcopy(matrix)
        self.m = m
        self.n = n

        for i in range(1, m):
            self.dp[i][0] = self.dp[i-1][0] + matrix[i][0]
        for i in range(1, n):
            self.dp[0][i] = self.dp[0][i-1] + matrix[0][i]

        for i in range(1, m):
            for j in range(1, n):
                self.dp[i][j] = self.dp[i-1][j] + self.dp[i][j-1] - self.dp[i-1][j-1] + matrix[i][j]

        for row in self.dp:
            print(str(row))

    def get_area(self, bottom, right):
        print("bottom = {}, right = {}".format(str(bottom), str(right)))
        if bottom < 0 or right < 0:
            print("return 0")
            return 0
        print("returning {}".format(str(self.dp[bottom][right])))
        return self.dp[bottom][right]

    def find_sum(self, l, r, u, d):
        assert(0 <= u <= d <= self.m)
        assert(0 <= l <= r <= self.n)
        return self.get_area(d, r) - self.get_area(u-1, r) - self.get_area(d, l-1) + self.get_area(u-1, l-1)


solver = Solver(matrix)
print(solver.find_sum(1, 2, 0, 1))
