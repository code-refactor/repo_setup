# 521_D. Shop

**ID:** 521_d_shop_3485
**Difficulty:** 10

## Description

Vasya plays one very well-known and extremely popular MMORPG game. His game character has k skill; currently the i-th of them equals to ai. Also this game has a common rating table in which the participants are ranked according to the product of all the skills of a hero in the descending order.

Vasya decided to 'upgrade' his character via the game store. This store offers n possible ways to improve the hero's skills; Each of these ways belongs to one of three types:

  1. assign the i-th skill to b; 
  2. add b to the i-th skill; 
  3. multiply the i-th skill by b. 



Unfortunately, a) every improvement can only be used once; b) the money on Vasya's card is enough only to purchase not more than m of the n improvements. Help Vasya to reach the highest ranking in the game. To do this tell Vasya which of improvements he has to purchase and in what order he should use them to make his rating become as high as possible. If there are several ways to achieve it, print any of them.

Input

The first line contains three numbers — k, n, m (1 ≤ k ≤ 105, 0 ≤ m ≤ n ≤ 105) — the number of skills, the number of improvements on sale and the number of them Vasya can afford.

The second line contains k space-separated numbers ai (1 ≤ ai ≤ 106), the initial values of skills.

Next n lines contain 3 space-separated numbers tj, ij, bj (1 ≤ tj ≤ 3, 1 ≤ ij ≤ k, 1 ≤ bj ≤ 106) — the type of the j-th improvement (1 for assigning, 2 for adding, 3 for multiplying), the skill to which it can be applied and the value of b for this improvement.

Output

The first line should contain a number l (0 ≤ l ≤ m) — the number of improvements you should use.

The second line should contain l distinct space-separated numbers vi (1 ≤ vi ≤ n) — the indices of improvements in the order in which they should be applied. The improvements are numbered starting from 1, in the order in which they appear in the input. 

Examples

Input

2 4 3
13 20
1 1 14
1 2 30
2 1 6
3 2 2


Output

3
2 3 4

## Categories

- greedy

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2 4 3
13 20
1 1 14
1 2 30
2 1 6
3 2 2
```

**Output**:
```
3
2 3 4
```

### Example 2

**Input**:
```
10 6 6
2 2 1 8 5 3 8 5 3 4
3 8 5
3 10 1
3 7 8
2 3 5
1 5 1
3 8 5
```

**Output**:
```
5
4 3 1 6 2
```

### Example 3

**Input**:
```
1 1 1
8
2 1 8
```

**Output**:
```
1
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
