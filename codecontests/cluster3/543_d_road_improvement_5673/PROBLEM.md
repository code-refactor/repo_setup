# 543_D. Road Improvement

**ID:** 543_d_road_improvement_5673
**Difficulty:** 10

## Description

The country has n cities and n - 1 bidirectional roads, it is possible to get from every city to any other one if you move only along the roads. The cities are numbered with integers from 1 to n inclusive.

All the roads are initially bad, but the government wants to improve the state of some roads. We will assume that the citizens are happy about road improvement if the path from the capital located in city x to any other city contains at most one bad road.

Your task is — for every possible x determine the number of ways of improving the quality of some roads in order to meet the citizens' condition. As those values can be rather large, you need to print each value modulo 1 000 000 007 (109 + 7).

Input

The first line of the input contains a single integer n (2 ≤ n ≤ 2·105) — the number of cities in the country. Next line contains n - 1 positive integers p2, p3, p4, ..., pn (1 ≤ pi ≤ i - 1) — the description of the roads in the country. Number pi means that the country has a road connecting city pi and city i. 

Output

Print n integers a1, a2, ..., an, where ai is the sought number of ways to improve the quality of the roads modulo 1 000 000 007 (109 + 7), if the capital of the country is at city number i.

Examples

Input

3
1 1


Output

4 3 3

Input

5
1 2 3 4


Output

5 8 9 8 5

## Categories

- dp
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3
1 1
```

**Output**:
```
4 3 3
```

### Example 2

**Input**:
```
5
1 2 3 4
```

**Output**:
```
5 8 9 8 5
```

### Example 3

**Input**:
```
137
1 1 3 3 5 5 7 8 8 10 10 12 12 14 14 16 16 18 18 20 21 21 23 23 25 26 26 28 28 30 30 32 33 33 35 36 36 38 38 40 41 41 43 43 45 46 46 48 49 49 51 51 53 53 55 56 56 58 59 59 61 62 62 64 64 66 67 67 1 1 71 71 73 73 75 76 76 78 78 80 80 82 82 84 84 86 86 88 89 89 91 91 93 94 94 96 96 98 98 100 101 101 103 104 104 106 106 108 109 109 111 111 113 114 114 116 117 117 119 119 121 121 123 124 124 126 127 127 129 130 130 132 132 134 135 135
```

**Output**:
```
1 500000005 500000005 750000007 750000007 875000008 875000008 0 1 62499998 31250000 93749994 46874998 109374986 54687494 117187470 58593736 121093688 60546845 123046749 124999808 62499905 125976240 62988121 126464261 126952280 63476141 127195898 63597950 127316924 63658463 127375871 127434816 63717409 127461155 127487492 63743747 127494392 63747197 127485305 127476216 63738109 127446596 63723299 127381635 127316672 63658337 127183887 127051100 63525551 126784098 63392050 126249380 63124691 125179587 124109792 62054897 121970025 119830256 59915129 115550631 111271004 55635503 102711708 51355855 85593095 68474480 34237241 34237241 500000005 500000005 750000007 750000007 875000008 875000008 0 1 62499998 31250000 93749994 46874998 109374986 54687494 117187470 58593736 121093688 60546845 123046749 124999808 62499905 125976240 62988121 126464261 126952280 63476141 127195898 63597950 127316924 63658463 127375871 127434816 63717409 127461155 127487492 63743747 127494392 63747197 127485305 127476216 63738109 127446596 63723299 127381635 127316672 63658337 127183887 127051100 63525551 126784098 63392050 126249380 63124691 125179587 124109792 62054897 121970025 119830256 59915129 115550631 111271004 55635503 102711708 51355855 85593095 68474480 34237241 34237241
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
