# 229_B. Planets

**ID:** 229_b_planets_4411
**Difficulty:** 8

## Description

Goa'uld Apophis captured Jack O'Neill's team again! Jack himself was able to escape, but by that time Apophis's ship had already jumped to hyperspace. But Jack knows on what planet will Apophis land. In order to save his friends, Jack must repeatedly go through stargates to get to this planet.

Overall the galaxy has n planets, indexed with numbers from 1 to n. Jack is on the planet with index 1, and Apophis will land on the planet with index n. Jack can move between some pairs of planets through stargates (he can move in both directions); the transfer takes a positive, and, perhaps, for different pairs of planets unequal number of seconds. Jack begins his journey at time 0.

It can be that other travellers are arriving to the planet where Jack is currently located. In this case, Jack has to wait for exactly 1 second before he can use the stargate. That is, if at time t another traveller arrives to the planet, Jack can only pass through the stargate at time t + 1, unless there are more travellers arriving at time t + 1 to the same planet.

Knowing the information about travel times between the planets, and the times when Jack would not be able to use the stargate on particular planets, determine the minimum time in which he can get to the planet with index n.

Input

The first line contains two space-separated integers: n (2 ≤ n ≤ 105), the number of planets in the galaxy, and m (0 ≤ m ≤ 105) — the number of pairs of planets between which Jack can travel using stargates. Then m lines follow, containing three integers each: the i-th line contains numbers of planets ai and bi (1 ≤ ai, bi ≤ n, ai ≠ bi), which are connected through stargates, and the integer transfer time (in seconds) ci (1 ≤ ci ≤ 104) between these planets. It is guaranteed that between any pair of planets there is at most one stargate connection.

Then n lines follow: the i-th line contains an integer ki (0 ≤ ki ≤ 105) that denotes the number of moments of time when other travellers arrive to the planet with index i. Then ki distinct space-separated integers tij (0 ≤ tij < 109) follow, sorted in ascending order. An integer tij means that at time tij (in seconds) another traveller arrives to the planet i. It is guaranteed that the sum of all ki does not exceed 105.

Output

Print a single number — the least amount of time Jack needs to get from planet 1 to planet n. If Jack can't get to planet n in any amount of time, print number -1.

Examples

Input

4 6
1 2 2
1 3 3
1 4 8
2 3 4
2 4 5
3 4 3
0
1 3
2 3 4
0


Output

7


Input

3 1
1 2 3
0
1 3
0


Output

-1

Note

In the first sample Jack has three ways to go from planet 1. If he moves to planet 4 at once, he spends 8 seconds. If he transfers to planet 3, he spends 3 seconds, but as other travellers arrive to planet 3 at time 3 and 4, he can travel to planet 4 only at time 5, thus spending 8 seconds in total. But if Jack moves to planet 2, and then — to planet 4, then he spends a total of only 2 + 5 = 7 seconds.

In the second sample one can't get from planet 1 to planet 3 by moving through stargates.

## Categories

- binary search
- data structures
- graphs
- shortest paths

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3 1
1 2 3
0
1 3
0
```

**Output**:
```
-1
```

### Example 2

**Input**:
```
4 6
1 2 2
1 3 3
1 4 8
2 3 4
2 4 5
3 4 3
0
1 3
2 3 4
0
```

**Output**:
```
7
```

### Example 3

**Input**:
```
3 3
1 2 3
2 3 2
1 3 7
0
4 3 4 5 6
0
```

**Output**:
```
7
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
