#!/usr/bin/env python3

from library import Solution, read_int, read_ints, mod_inverse, mod_add, mod_mul, MOD2, fast_input

# Use fast input for performance
input = fast_input()

class SlimeBiscuits(Solution):
    def __init__(self):
        super().__init__(mod=MOD2)
        
    def read_input(self):
        self.n = read_int()
        self.a = read_ints()
        self.tot = sum(self.a)
        # dp[i][0] and dp[i][1] are the coefficients in the linear equation system
        self.dp = [[0, 0] for _ in range(self.tot + 1)]
        
    def solve(self):
        # Base cases
        self.dp[0] = [0, 1]
        self.dp[1] = [(1 - self.n) % self.mod, 1]
        
        # Fill the DP table
        for k in range(1, self.tot):
            temp = mod_inverse(self.tot - k, self.mod)
            
            # Calculate dp[k+1][0]
            dp_k_plus_1_0 = -self.tot * (self.n - 1)
            dp_k_plus_1_0 -= self.dp[k][0] * (2*k - self.tot - k*self.n)
            dp_k_plus_1_0 -= self.dp[k-1][0] * k * (self.n - 1)
            dp_k_plus_1_0 = mod_mul(dp_k_plus_1_0, temp, self.mod)
            self.dp[k+1][0] = dp_k_plus_1_0
            
            # Calculate dp[k+1][1]
            dp_k_plus_1_1 = -self.dp[k][1] * (2*k - self.tot - k*self.n)
            dp_k_plus_1_1 -= self.dp[k-1][1] * k * (self.n - 1)
            dp_k_plus_1_1 = mod_mul(dp_k_plus_1_1, temp, self.mod)
            self.dp[k+1][1] = dp_k_plus_1_1
        
        # Calculate alpha
        alpha = mod_mul(-self.dp[self.tot][0], mod_inverse(self.dp[self.tot][1], self.mod), self.mod)
        
        # Calculate final answer
        ans = 0
        for i in range(self.n):
            term = mod_add(self.dp[self.a[i]][0], mod_mul(self.dp[self.a[i]][1], alpha, self.mod), self.mod)
            ans = mod_add(ans, term, self.mod)
            
        ans = mod_add(ans, -mod_mul(alpha, self.n - 1, self.mod), self.mod)
        ans = mod_mul(ans, mod_inverse(self.n, self.mod), self.mod)
        
        return ans

if __name__ == "__main__":
    solution = SlimeBiscuits()
    solution.run()