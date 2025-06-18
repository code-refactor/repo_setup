# 597_C. Subsequences

**ID:** 597_c_subsequences_6091
**Difficulty:** 9

## Description

For the given sequence with n different elements find the number of increasing subsequences with k + 1 elements. It is guaranteed that the answer is not greater than 8·1018.

Input

First line contain two integer values n and k (1 ≤ n ≤ 105, 0 ≤ k ≤ 10) — the length of sequence and the number of elements in increasing subsequences.

Next n lines contains one integer ai (1 ≤ ai ≤ n) each — elements of sequence. All values ai are different.

Output

Print one integer — the answer to the problem.

Examples

Input

5 2
1
2
3
5
4


Output

7

## Categories

- data structures
- dp

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5 2
1
2
3
5
4
```

**Output**:
```
7
```

### Example 2

**Input**:
```
10 2
6
10
9
7
1
2
8
5
4
3
```

**Output**:
```
5
```

### Example 3

**Input**:
```
100 7
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
```

**Output**:
```
186087894300
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
