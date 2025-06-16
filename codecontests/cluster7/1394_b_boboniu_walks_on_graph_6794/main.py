from library import read_ints, read_matrix, xor_array
from random import randrange
import sys
input = sys.stdin.buffer.readline

def solve(digit, res):
    ans = 0
    if digit == k:
        return int(res == zob_all)
    for i in range(digit + 1):
        ans += solve(digit + 1, res ^ zob[digit][i])
    return ans

n, m, k = read_ints()
edges = read_matrix(m)
LIMIT = (1 << 31) - 1
OFFSET = 10 ** 6


graph = [[] for i in range(n)]
for u, v, cost in edges:
    u -= 1
    v -= 1
    graph[u].append(cost * OFFSET + v)

hashes = [randrange(0, LIMIT + 1) for i in range(n)]

zob = [[0] * k for i in range(k)]
zob_all = xor_array(hashes)

for v in range(n):
    deg = len(graph[v])
    graph[v] = sorted(graph[v])
    for i, tmp in enumerate(graph[v]):
        nxt_v = tmp % OFFSET
        zob[deg - 1][i] ^= hashes[nxt_v]

print(solve(0, 0))