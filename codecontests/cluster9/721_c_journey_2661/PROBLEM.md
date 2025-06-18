# 721_C. Journey

**ID:** 721_c_journey_2661
**Difficulty:** 9

## Description

Recently Irina arrived to one of the most famous cities of Berland — the Berlatov city. There are n showplaces in the city, numbered from 1 to n, and some of them are connected by one-directional roads. The roads in Berlatov are designed in a way such that there are no cyclic routes between showplaces.

Initially Irina stands at the showplace 1, and the endpoint of her journey is the showplace n. Naturally, Irina wants to visit as much showplaces as she can during her journey. However, Irina's stay in Berlatov is limited and she can't be there for more than T time units.

Help Irina determine how many showplaces she may visit during her journey from showplace 1 to showplace n within a time not exceeding T. It is guaranteed that there is at least one route from showplace 1 to showplace n such that Irina will spend no more than T time units passing it.

Input

The first line of the input contains three integers n, m and T (2 ≤ n ≤ 5000, 1 ≤ m ≤ 5000, 1 ≤ T ≤ 109) — the number of showplaces, the number of roads between them and the time of Irina's stay in Berlatov respectively.

The next m lines describes roads in Berlatov. i-th of them contains 3 integers ui, vi, ti (1 ≤ ui, vi ≤ n, ui ≠ vi, 1 ≤ ti ≤ 109), meaning that there is a road starting from showplace ui and leading to showplace vi, and Irina spends ti time units to pass it. It is guaranteed that the roads do not form cyclic routes.

It is guaranteed, that there is at most one road between each pair of showplaces.

Output

Print the single integer k (2 ≤ k ≤ n) — the maximum number of showplaces that Irina can visit during her journey from showplace 1 to showplace n within time not exceeding T, in the first line.

Print k distinct integers in the second line — indices of showplaces that Irina will visit on her route, in the order of encountering them.

If there are multiple answers, print any of them.

Examples

Input

4 3 13
1 2 5
2 3 7
2 4 8


Output

3
1 2 4 


Input

6 6 7
1 2 2
1 3 3
3 6 3
2 4 2
4 6 2
6 5 1


Output

4
1 2 4 6 


Input

5 5 6
1 3 3
3 5 3
1 2 2
2 4 3
4 5 2


Output

3
1 3 5 

## Categories

- dp
- graphs

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
4 3 13
1 2 5
2 3 7
2 4 8
```

**Output**:
```
3
1 2 4
```

### Example 2

**Input**:
```
6 6 7
1 2 2
1 3 3
3 6 3
2 4 2
4 6 2
6 5 1
```

**Output**:
```
4
1 2 4 6
```

### Example 3

**Input**:
```
5 5 6
1 3 3
3 5 3
1 2 2
2 4 3
4 5 2
```

**Output**:
```
3
1 3 5
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
