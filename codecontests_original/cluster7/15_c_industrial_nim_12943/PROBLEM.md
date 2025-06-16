# 15_C. Industrial Nim

**ID:** 15_c_industrial_nim_12943
**Difficulty:** 9

## Description

There are n stone quarries in Petrograd.

Each quarry owns mi dumpers (1 ≤ i ≤ n). It is known that the first dumper of the i-th quarry has xi stones in it, the second dumper has xi + 1 stones in it, the third has xi + 2, and the mi-th dumper (the last for the i-th quarry) has xi + mi - 1 stones in it.

Two oligarchs play a well-known game Nim. Players take turns removing stones from dumpers. On each turn, a player can select any dumper and remove any non-zero amount of stones from it. The player who cannot take a stone loses.

Your task is to find out which oligarch will win, provided that both of them play optimally. The oligarchs asked you not to reveal their names. So, let's call the one who takes the first stone «tolik» and the other one «bolik».

Input

The first line of the input contains one integer number n (1 ≤ n ≤ 105) — the amount of quarries. Then there follow n lines, each of them contains two space-separated integers xi and mi (1 ≤ xi, mi ≤ 1016) — the amount of stones in the first dumper of the i-th quarry and the number of dumpers at the i-th quarry.

Output

Output «tolik» if the oligarch who takes a stone first wins, and «bolik» otherwise.

Examples

Input

2
2 1
3 2


Output

tolik


Input

4
1 1
1 1
1 1
1 1


Output

bolik

## Categories

- games

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2
2 1
3 2
```

**Output**:
```
tolik
```

### Example 2

**Input**:
```
4
1 1
1 1
1 1
1 1
```

**Output**:
```
bolik
```

### Example 3

**Input**:
```
30
53 12
13 98
21 60
76 58
39 5
62 58
73 80
13 75
37 45
44 86
1 85
13 33
17 50
12 26
97 48
52 40
2 71
95 79
38 76
24 54
91 39
97 92
94 80
50 61
33 56
22 91
39 94
31 56
28 16
20 44
```

**Output**:
```
tolik
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
