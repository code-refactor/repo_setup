# 99_D. Help King

**ID:** 99_d_help_king_8501
**Difficulty:** 10

## Description

This is the modification of the problem used during the official round. Unfortunately, author's solution of the original problem appeared wrong, so the problem was changed specially for the archive.

Once upon a time in a far away kingdom lived the King. The King had a beautiful daughter, Victoria. They lived happily, but not happily ever after: one day a vicious dragon attacked the kingdom and stole Victoria. The King was full of grief, yet he gathered his noble knights and promised half of his kingdom and Victoria's hand in marriage to the one who will save the girl from the infernal beast.

Having travelled for some time, the knights found the dragon's lair and all of them rushed there to save Victoria. Each knight spat on the dragon once and, as the dragon had quite a fragile and frail heart, his heart broke and poor beast died. As for the noble knights, they got Victoria right to the King and started brawling as each one wanted the girl's hand in marriage.

The problem was that all the noble knights were equally noble and equally handsome, and Victoria didn't want to marry any of them anyway. Then the King (and he was a very wise man and didn't want to hurt anybody's feelings) decided to find out who will get his daughter randomly, i.e. tossing a coin. However, there turned out to be n noble knights and the coin only has two sides. The good thing is that when a coin is tossed, the coin falls on each side with equal probability. The King got interested how to pick one noble knight using this coin so that all knights had equal probability of being chosen (the probability in that case should always be equal to 1 / n). First the King wants to know the expected number of times he will need to toss a coin to determine the winner. Besides, while tossing the coin, the King should follow the optimal tossing strategy (i.e. the strategy that minimizes the expected number of tosses). Help the King in this challenging task.

Input

The first line contains a single integer n from the problem's statement (1 ≤ n ≤ 10000).

Output

Print the sought expected number of tosses as an irreducible fraction in the following form: "a/b" (without the quotes) without leading zeroes.

Examples

Input

2


Output

1/1


Input

3


Output

8/3


Input

4


Output

2/1

## Categories

- implementation
- probabilities
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3
```

**Output**:
```
8/3
```

### Example 2

**Input**:
```
2
```

**Output**:
```
1/1
```

### Example 3

**Input**:
```
4
```

**Output**:
```
2/1
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
