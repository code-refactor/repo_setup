# 1141_A. Game 23

**ID:** 1141_a_game_23_2618
**Difficulty:** very hard

## Description

Polycarp plays "Game 23". Initially he has a number n and his goal is to transform it to m. In one move, he can multiply n by 2 or multiply n by 3. He can perform any number of moves.

Print the number of moves needed to transform n to m. Print -1 if it is impossible to do so.

It is easy to prove that any way to transform n to m contains the same number of moves (i.e. number of moves doesn't depend on the way of transformation).

Input

The only line of the input contains two integers n and m (1 ≤ n ≤ m ≤ 5⋅10^8).

Output

Print the number of moves to transform n to m, or -1 if there is no solution.

Examples

Input


120 51840


Output


7


Input


42 42


Output


0


Input


48 72


Output


-1

Note

In the first example, the possible sequence of moves is: 120 → 240 → 720 → 1440 → 4320 → 12960 → 25920 → 51840. The are 7 steps in total.

In the second example, no moves are needed. Thus, the answer is 0.

In the third example, it is impossible to transform 48 to 72.

## Categories

- implementation
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
42 42
```

**Output**:
```
0
```

### Example 2

**Input**:
```
48 72
```

**Output**:
```
-1
```

### Example 3

**Input**:
```
120 51840
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
