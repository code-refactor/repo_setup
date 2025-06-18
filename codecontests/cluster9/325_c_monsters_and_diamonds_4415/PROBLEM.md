# 325_C. Monsters and Diamonds

**ID:** 325_c_monsters_and_diamonds_4415
**Difficulty:** 9

## Description

Piegirl has found a monster and a book about monsters and pies. When she is reading the book, she found out that there are n types of monsters, each with an ID between 1 and n. If you feed a pie to a monster, the monster will split into some number of monsters (possibly zero), and at least one colorful diamond. Monsters may be able to split in multiple ways.

At the begining Piegirl has exactly one monster. She begins by feeding the monster a pie. She continues feeding pies to monsters until no more monsters are left. Then she collects all the diamonds that were created.

You will be given a list of split rules describing the way in which the various monsters can split. Every monster can split in at least one way, and if a monster can split in multiple ways then each time when it splits Piegirl can choose the way it splits.

For each monster, determine the smallest and the largest number of diamonds Piegirl can possibly collect, if initially she has a single instance of that monster. Piegirl has an unlimited supply of pies.

Input

The first line contains two integers: m and n (1 ≤ m, n ≤ 105), the number of possible splits and the number of different monster types. Each of the following m lines contains a split rule. Each split rule starts with an integer (a monster ID) mi (1 ≤ mi ≤ n), and a positive integer li indicating the number of monsters and diamonds the current monster can split into. This is followed by li integers, with positive integers representing a monster ID and -1 representing a diamond.

Each monster will have at least one split rule. Each split rule will have at least one diamond. The sum of li across all split rules will be at most 105.

Output

For each monster, in order of their IDs, print a line with two integers: the smallest and the largest number of diamonds that can possibly be collected by starting with that monster. If Piegirl cannot possibly end up in a state without monsters, print -1 for both smallest and the largest value. If she can collect an arbitrarily large number of diamonds, print -2 as the largest number of diamonds. 

If any number in output exceeds 314000000 (but is finite), print 314000000 instead of that number.

Examples

Input

6 4
1 3 -1 1 -1
1 2 -1 -1
2 3 -1 3 -1
2 3 -1 -1 -1
3 2 -1 -1
4 2 4 -1


Output

2 -2
3 4
2 2
-1 -1


Input

3 2
1 2 1 -1
2 2 -1 -1
2 3 2 1 -1


Output

-1 -1
2 2

## Categories

- dfs and similar
- graphs
- shortest paths

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3 2
1 2 1 -1
2 2 -1 -1
2 3 2 1 -1
```

**Output**:
```
-1 -1
2 2
```

### Example 2

**Input**:
```
6 4
1 3 -1 1 -1
1 2 -1 -1
2 3 -1 3 -1
2 3 -1 -1 -1
3 2 -1 -1
4 2 4 -1
```

**Output**:
```
2 -2
3 4
2 2
-1 -1
```

### Example 3

**Input**:
```
4 1
1 3 -1 -1 -1
1 2 -1 -1
1 4 -1 -1 -1 -1
1 3 -1 -1 -1
```

**Output**:
```
2 4
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
