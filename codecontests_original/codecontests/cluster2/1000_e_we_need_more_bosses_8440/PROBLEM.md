# 1000_E. We Need More Bosses

**ID:** 1000_e_we_need_more_bosses_8440
**Difficulty:** 11

## Description

Your friend is developing a computer game. He has already decided how the game world should look like — it should consist of n locations connected by m two-way passages. The passages are designed in such a way that it should be possible to get from any location to any other location.

Of course, some passages should be guarded by the monsters (if you just can go everywhere without any difficulties, then it's not fun, right?). Some crucial passages will be guarded by really fearsome monsters, requiring the hero to prepare for battle and designing his own tactics of defeating them (commonly these kinds of monsters are called bosses). And your friend wants you to help him place these bosses.

The game will start in location s and end in location t, but these locations are not chosen yet. After choosing these locations, your friend will place a boss in each passage such that it is impossible to get from s to t without using this passage. Your friend wants to place as much bosses as possible (because more challenges means more fun, right?), so he asks you to help him determine the maximum possible number of bosses, considering that any location can be chosen as s or as t.

Input

The first line contains two integers n and m (2 ≤ n ≤ 3 ⋅ 10^5, n - 1 ≤ m ≤ 3 ⋅ 10^5) — the number of locations and passages, respectively.

Then m lines follow, each containing two integers x and y (1 ≤ x, y ≤ n, x ≠ y) describing the endpoints of one of the passages.

It is guaranteed that there is no pair of locations directly connected by two or more passages, and that any location is reachable from any other location.

Output

Print one integer — the maximum number of bosses your friend can place, considering all possible choices for s and t.

Examples

Input

5 5
1 2
2 3
3 1
4 1
5 2


Output

2


Input

4 3
1 2
4 3
3 2


Output

3

## Categories

- dfs and similar
- graphs
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5 5
1 2
2 3
3 1
4 1
5 2
```

**Output**:
```
2
```

### Example 2

**Input**:
```
4 3
1 2
4 3
3 2
```

**Output**:
```
3
```

### Example 3

**Input**:
```
5 6
1 5
2 3
3 5
2 1
2 5
2 4
```

**Output**:
```
1
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
