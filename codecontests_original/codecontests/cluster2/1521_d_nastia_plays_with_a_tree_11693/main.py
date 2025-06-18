#!/usr/bin/env python3

def dfs(x, e, v, g):
  v[x] = True
  c = 0
  for y in e[x]:
    if not y in v:
      if dfs(y, e, v, g):
        c += 1
        if c > 2:
          g.append((x, y))
      else:
        g.append((x, y))

  if c < 2:
    return True

  if x != 1:
    return False

def leaf(x, e):
  p = 0
  while True:
    u = 0
    for y in e[x]:
      if y != p:
        u = y
        break
    if u == 0: break
    p = x
    x = u
  return x

def solve(n, e):
  g = []
  dfs(1, e, {}, g)

  for x, y in g:
    e[x].remove(y)
    e[y].remove(x)

  z = []
  l = leaf(1, e)
  for p, y, in g:
    r = leaf(y, e)
    z.append((p, y, l, r))
    l = leaf(r, e)

  print(len(z))
  if len(z) > 0:
    print('\n'.join(map(lambda x: ' '.join(map(str, x)), z)))


def main():
  t = int(input())
  for i in range(t):
    n = int(input())
    e = {}
    for i in range(n - 1):
      a, b = map(int, input().split())
      if not a in e: e[a] = []
      if not b in e: e[b] = []
      e[a].append(b)
      e[b].append(a)
    solve(n, e)


import threading
import sys

sys.setrecursionlimit(10 ** 5 + 1)
threading.stack_size(262000)
main = threading.Thread(target=main)
main.start()
main.join()
