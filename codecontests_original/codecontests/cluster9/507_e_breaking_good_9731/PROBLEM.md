# 507_E. Breaking Good

**ID:** 507_e_breaking_good_9731
**Difficulty:** 11

## Description

Breaking Good is a new video game which a lot of gamers want to have. There is a certain level in the game that is really difficult even for experienced gamers.

Walter William, the main character of the game, wants to join a gang called Los Hermanos (The Brothers). The gang controls the whole country which consists of n cities with m bidirectional roads connecting them. There is no road is connecting a city to itself and for any two cities there is at most one road between them. The country is connected, in the other words, it is possible to reach any city from any other city using the given roads. 

The roads aren't all working. There are some roads which need some more work to be performed to be completely functioning.

The gang is going to rob a bank! The bank is located in city 1. As usual, the hardest part is to escape to their headquarters where the police can't get them. The gang's headquarters is in city n. To gain the gang's trust, Walter is in charge of this operation, so he came up with a smart plan.

First of all the path which they are going to use on their way back from city 1 to their headquarters n must be as short as possible, since it is important to finish operation as fast as possible.

Then, gang has to blow up all other roads in country that don't lay on this path, in order to prevent any police reinforcements. In case of non-working road, they don't have to blow up it as it is already malfunctional. 

If the chosen path has some roads that doesn't work they'll have to repair those roads before the operation.

Walter discovered that there was a lot of paths that satisfied the condition of being shortest possible so he decided to choose among them a path that minimizes the total number of affected roads (both roads that have to be blown up and roads to be repaired).

Can you help Walter complete his task and gain the gang's trust?

Input

The first line of input contains two integers n, m (2 ≤ n ≤ 105, <image>), the number of cities and number of roads respectively.

In following m lines there are descriptions of roads. Each description consists of three integers x, y, z (1 ≤ x, y ≤ n, <image>) meaning that there is a road connecting cities number x and y. If z = 1, this road is working, otherwise it is not.

Output

In the first line output one integer k, the minimum possible number of roads affected by gang.

In the following k lines output three integers describing roads that should be affected. Each line should contain three integers x, y, z (1 ≤ x, y ≤ n, <image>), cities connected by a road and the new state of a road. z = 1 indicates that the road between cities x and y should be repaired and z = 0 means that road should be blown up. 

You may output roads in any order. Each affected road should appear exactly once. You may output cities connected by a single road in any order. If you output a road, it's original state should be different from z.

After performing all operations accroding to your plan, there should remain working only roads lying on some certain shortest past between city 1 and n.

If there are multiple optimal answers output any.

Examples

Input

2 1
1 2 0


Output

1
1 2 1


Input

4 4
1 2 1
1 3 0
2 3 1
3 4 1


Output

3
1 2 0
1 3 1
2 3 0


Input

8 9
1 2 0
8 3 0
2 3 1
1 4 1
8 7 0
1 5 1
4 6 1
5 7 0
6 8 0


Output

3
2 3 0
1 5 0
6 8 1

Note

In the first test the only path is 1 - 2

In the second test the only shortest path is 1 - 3 - 4

In the third test there are multiple shortest paths but the optimal is 1 - 4 - 6 - 8

## Categories

- dfs and similar
- dp
- graphs
- shortest paths

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2 1
1 2 0
```

**Output**:
```
1
1 2 1
```

### Example 2

**Input**:
```
8 9
1 2 0
8 3 0
2 3 1
1 4 1
8 7 0
1 5 1
4 6 1
5 7 0
6 8 0
```

**Output**:
```
3
2 3 0
1 5 0
6 8 1
```

### Example 3

**Input**:
```
4 4
1 2 1
1 3 0
2 3 1
3 4 1
```

**Output**:
```
3
1 2 0
1 3 1
2 3 0
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
