#!/usr/bin/env python3

from library import read_int_tuple, bootstrap

def main():
    n, k = read_int_tuple()
    MOD = 1000000007
    cnt = [[[0] * 21 for _ in (0, 1)] for _ in range(n + 1)]
    
    # Create adjacency list
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = read_int_tuple()
        adj[u].append((v, 1))
        adj[v].append((u, 1))
    
    @bootstrap
    def dfs(u, parent):
        # Initialize: cnt[u][0][0] = not painted, distance 0
        #            cnt[u][1][k] = painted, distance k
        cnt[u][0][0] = cnt[u][1][k] = 1
        
        for v, _ in adj[u]:
            if v != parent:
                yield dfs(v, u)
                tmp0, tmp1 = [0] * 21, [0] * 21
                
                for i in range(k + 1):
                    for j in range(k + 1):
                        # Node u not painted, v not painted
                        if i != k:
                            tmp0[j if i < j else i + 1] += cnt[u][0][j] * cnt[v][0][i]
                        
                        # Node u painted, v not painted
                        if i < j:
                            tmp1[j] += cnt[u][1][j] * cnt[v][0][i]
                        elif i != k:
                            tmp0[i + 1] += cnt[u][1][j] * cnt[v][0][i]
                        
                        # Node u not painted, v painted
                        if i > j:
                            tmp1[i - 1] += cnt[u][0][j] * cnt[v][1][i]
                        else:
                            tmp0[j] += cnt[u][0][j] * cnt[v][1][i]
                        
                        # Node u painted, v painted
                        tmp1[max(i - 1, j)] += cnt[u][1][j] * cnt[v][1][i]
                
                # Apply modulo to prevent overflow
                for i in range(21):
                    tmp0[i] %= MOD
                    tmp1[i] %= MOD
                
                cnt[u][0] = tmp0
                cnt[u][1] = tmp1
        yield
    
    dfs(1, -1)
    print(sum(cnt[1][1][j] for j in range(k + 1)) % MOD)

if __name__ == '__main__':
    main()
