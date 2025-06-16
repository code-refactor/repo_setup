def read_ints():
    return list(map(int, input().split()))

def read_matrix(n, m=None):
    if m is None:
        return [list(map(int, input().split())) for _ in range(n)]
    return [[int(input().split()[j]) for j in range(m)] for _ in range(n)]

def read_array(n):
    return list(map(int, input().split()))

def xor_range(l, r):
    def xor_up_to(n):
        return [n, 1, n+1, 0][n % 4]
    return xor_up_to(r) ^ xor_up_to(l-1)

def xor_array(arr):
    result = 0
    for x in arr:
        result ^= x
    return result

def prefix_xor(arr):
    pref = [0]
    for x in arr:
        pref.append(pref[-1] ^ x)
    return pref

def bit_count(n):
    return bin(n).count('1')

def get_bit(n, i):
    return (n >> i) & 1

def highest_bit(n):
    if n == 0:
        return -1
    return n.bit_length() - 1

def trailing_zeros(n):
    if n % 2 == 1:
        return 0
    else:
        return 1 + trailing_zeros(n // 2)

def validate_xor_sum(total, target):
    return total >= target and (total - target) % 2 == 0

class CountingXORTrie:
    def __init__(self, max_bits=30):
        self.max_bits = max_bits
        self.tree = [[0, 0, 0]]
        
    def insert(self, x):
        now = 0
        self.tree[now][2] += 1
        for i in range(self.max_bits - 1, -1, -1):
            bit = (x >> i) & 1
            if self.tree[now][bit] == 0:
                self.tree[now][bit] = len(self.tree)
                self.tree.append([0, 0, 0])
            now = self.tree[now][bit]
            self.tree[now][2] += 1
    
    def query_min_xor_remove(self, x):
        now = ans = 0
        for i in range(self.max_bits - 1, -1, -1):
            bit = (x >> i) & 1
            if self.tree[now][bit] and self.tree[self.tree[now][bit]][2]:
                now = self.tree[now][bit]
            else:
                now = self.tree[now][bit ^ 1]
                ans |= (1 << i)
            self.tree[now][2] -= 1
        return ans
