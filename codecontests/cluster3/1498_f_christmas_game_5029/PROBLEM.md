# 1498_F. Christmas Game

**ID:** 1498_f_christmas_game_5029
**Difficulty:** 12

## Description

Alice and Bob are going to celebrate Christmas by playing a game with a tree of presents. The tree has n nodes (numbered 1 to n, with some node r as its root). There are a_i presents are hanging from the i-th node.

Before beginning the game, a special integer k is chosen. The game proceeds as follows:

  * Alice begins the game, with moves alternating each turn;
  * in any move, the current player may choose some node (for example, i) which has depth at least k. Then, the player picks some positive number of presents hanging from that node, let's call it m (1 ≤ m ≤ a_i);
  * the player then places these m presents on the k-th ancestor (let's call it j) of the i-th node (the k-th ancestor of vertex i is a vertex j such that i is a descendant of j, and the difference between the depth of j and the depth of i is exactly k). Now, the number of presents of the i-th node (a_i) is decreased by m, and, correspondingly, a_j is increased by m;
  * Alice and Bob both play optimally. The player unable to make a move loses the game.



For each possible root of the tree, find who among Alice or Bob wins the game.

Note: The depth of a node i in a tree with root r is defined as the number of edges on the simple path from node r to node i. The depth of root r itself is zero.

Input

The first line contains two space-separated integers n and k (3 ≤ n ≤ 10^5, 1 ≤ k ≤ 20).

The next n-1 lines each contain two integers x and y (1 ≤ x, y ≤ n, x ≠ y), denoting an undirected edge between the two nodes x and y. These edges form a tree of n nodes.

The next line contains n space-separated integers denoting the array a (0 ≤ a_i ≤ 10^9).

Output

Output n integers, where the i-th integer is 1 if Alice wins the game when the tree is rooted at node i, or 0 otherwise.

Example

Input


5 1
1 2
1 3
5 2
4 3
0 3 2 4 4


Output


1 0 0 1 1 

Note

Let us calculate the answer for sample input with root node as 1 and as 2.

Root node 1

Alice always wins in this case. One possible gameplay between Alice and Bob is:

  * Alice moves one present from node 4 to node 3. 
  * Bob moves four presents from node 5 to node 2. 
  * Alice moves four presents from node 2 to node 1. 
  * Bob moves three presents from node 2 to node 1. 
  * Alice moves three presents from node 3 to node 1. 
  * Bob moves three presents from node 4 to node 3. 
  * Alice moves three presents from node 3 to node 1. 



Bob is now unable to make a move and hence loses.

Root node 2

Bob always wins in this case. One such gameplay is:

  * Alice moves four presents from node 4 to node 3. 
  * Bob moves four presents from node 5 to node 2. 
  * Alice moves six presents from node 3 to node 1. 
  * Bob moves six presents from node 1 to node 2. 



Alice is now unable to make a move and hence loses.

## Categories

- bitmasks
- data structures
- dfs and similar
- dp
- games
- math
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5 1
1 2
1 3
5 2
4 3
0 3 2 4 4
```

**Output**:
```
1 0 0 1 1
```

### Example 2

**Input**:
```
3 3
1 3
1 2
1 2 3
```

**Output**:
```
0 0 0
```

### Example 3

**Input**:
```
3 1
3 1
3 2
1 2 3
```

**Output**:
```
1 1 1
```


## Testing

Run the solution with:

```bash
./run.sh
```

Or test with a specific input file:

```bash
uv run main.py < tests/input_1.txt
```
