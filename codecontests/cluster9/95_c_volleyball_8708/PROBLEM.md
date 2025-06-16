# 95_C. Volleyball

**ID:** 95_c_volleyball_8708
**Difficulty:** 9

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
15 29
6 6
7 12 7
11 3 7
4 5 18
13 9 18
3 8 12
6 1 7
4 1 4
12 5 18
10 8 15
2 10 1
9 7 11
2 4 10
2 14 3
15 12 14
1 13 8
11 4 1
15 11 2
1 5 9
5 2 5
9 10 5
15 2 17
11 5 1
14 15 14
10 1 16
15 9 2
13 15 6
13 5 1
7 12 6
12 5 13
8 26
35 17
16 14
12 13
21 1
31 9
7 24
11 31
29 5
16 22
29 7
30 20
36 3
26 22
37 6
```

**Output**:
```
0
```

### Example 3

**Input**:
```
7 15
5 5
3 4 6
7 4 3
7 2 8
2 5 2
7 2 8
5 2 9
3 1 7
1 2 4
7 1 8
7 5 7
2 4 2
4 3 9
7 4 2
5 4 8
7 2 8
15 4
18 18
6 8
16 5
11 1
5 3
18 4
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
