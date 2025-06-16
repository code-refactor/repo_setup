#!/usr/bin/env python3

if __name__ == '__main__':
    n = int(input())
    nonleaf = [0 for i in range(1010)]
    child = [[] for i in range(1010)]
    leaf = [0 for i in range(1010)]

    def dfs(s):
        cnt = 0
        for chd in child[s]:
            cnt += dfs(chd)
        leaf[s] = cnt
        return 1 - nonleaf[s]

    for i in range(2, n + 1):
        node = int(input())
        child[node].append(i)
        nonleaf[node] = 1

    dfs(1)

    # print(nonleaf[1:n + 1])
    # print(child[1:n + 1])
    # print(leaf[1:n + 1])

    for i in range(1, n + 1):
        if nonleaf[i] and leaf[i] < 3:
            print("No")
            exit()

    print("Yes")

          	 		  	 		   				 	 	