# 96_D. Volleyball

**ID:** 96_d_volleyball_6419
**Difficulty:** 10

## Description

Petya loves volleyball very much. One day he was running late for a volleyball match. Petya hasn't bought his own car yet, that's why he had to take a taxi. The city has n junctions, some of which are connected by two-way roads. The length of each road is defined by some positive integer number of meters; the roads can have different lengths.

Initially each junction has exactly one taxi standing there. The taxi driver from the i-th junction agrees to drive Petya (perhaps through several intermediate junctions) to some other junction if the travel distance is not more than ti meters. Also, the cost of the ride doesn't depend on the distance and is equal to ci bourles. Taxis can't stop in the middle of a road. Each taxi can be used no more than once. Petya can catch taxi only in the junction, where it stands initially.

At the moment Petya is located on the junction x and the volleyball stadium is on the junction y. Determine the minimum amount of money Petya will need to drive to the stadium.

Input

The first line contains two integers n and m (1 ≤ n ≤ 1000, 0 ≤ m ≤ 1000). They are the number of junctions and roads in the city correspondingly. The junctions are numbered from 1 to n, inclusive. The next line contains two integers x and y (1 ≤ x, y ≤ n). They are the numbers of the initial and final junctions correspondingly. Next m lines contain the roads' description. Each road is described by a group of three integers ui, vi, wi (1 ≤ ui, vi ≤ n, 1 ≤ wi ≤ 109) — they are the numbers of the junctions connected by the road and the length of the road, correspondingly. The next n lines contain n pairs of integers ti and ci (1 ≤ ti, ci ≤ 109), which describe the taxi driver that waits at the i-th junction — the maximum distance he can drive and the drive's cost. The road can't connect the junction with itself, but between a pair of junctions there can be more than one road. All consecutive numbers in each line are separated by exactly one space character.

Output

If taxis can't drive Petya to the destination point, print "-1" (without the quotes). Otherwise, print the drive's minimum cost.

Please do not use the %lld specificator to read or write 64-bit integers in С++. It is preferred to use cin, cout streams or the %I64d specificator.

Examples

Input

4 4
1 3
1 2 3
1 4 1
2 4 1
2 3 5
2 7
7 2
1 2
7 7


Output

9

Note

An optimal way — ride from the junction 1 to 2 (via junction 4), then from 2 to 3. It costs 7+2=9 bourles.

## Categories

- shortest paths

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
4 4
1 3
1 2 3
1 4 1
2 4 1
2 3 5
2 7
7 2
1 2
7 7
```

**Output**:
```
9
```

### Example 2

**Input**:
```
5 7
1 3
1 2 1
1 3 3
1 5 1
1 4 2
5 4 3
3 5 2
2 3 8
2 7
10 3
4 7
2 1
1 1
```

**Output**:
```
10
```

### Example 3

**Input**:
```
3 2
3 3
1 2 2
1 3 3
2 7
2 7
3 7
```

**Output**:
```
0
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
