# 306_C. White, Black and White Again

**ID:** 306_c_white_black_and_white_again_245
**Difficulty:** 9

## Description

Polycarpus is sure that his life fits the description: "first there is a white stripe, then a black one, then a white one again". So, Polycarpus is sure that this rule is going to fulfill during the next n days. Polycarpus knows that he is in for w good events and b not-so-good events. At least one event is going to take place during each day. As each day is unequivocally characterizes as a part of a white or a black stripe, then each day is going to have events of the same type only (ether good or not-so-good).

What is the number of distinct ways this scenario can develop over the next n days if Polycarpus is in for a white stripe (a stripe that has good events only, the stripe's length is at least 1 day), the a black stripe (a stripe that has not-so-good events only, the stripe's length is at least 1 day) and a white stripe again (a stripe that has good events only, the stripe's length is at least 1 day). Each of n days will belong to one of the three stripes only.

Note that even the events of the same type are distinct from each other. Even if some events occur on the same day, they go in some order (there are no simultaneous events).

Write a code that prints the number of possible configurations to sort the events into days. See the samples for clarifications on which scenarios should be considered distinct. Print the answer modulo 1000000009 (109 + 9).

Input

The single line of the input contains integers n, w and b (3 ≤ n ≤ 4000, 2 ≤ w ≤ 4000, 1 ≤ b ≤ 4000) — the number of days, the number of good events and the number of not-so-good events. It is guaranteed that w + b ≥ n.

Output

Print the required number of ways modulo 1000000009 (109 + 9).

Examples

Input

3 2 1


Output

2


Input

4 2 2


Output

4


Input

3 2 2


Output

4

Note

We'll represent the good events by numbers starting from 1 and the not-so-good events — by letters starting from 'a'. Vertical lines separate days.

In the first sample the possible ways are: "1|a|2" and "2|a|1". In the second sample the possible ways are: "1|a|b|2", "2|a|b|1", "1|b|a|2" and "2|b|a|1". In the third sample the possible ways are: "1|ab|2", "2|ab|1", "1|ba|2" and "2|ba|1".

## Categories

- combinatorics
- number theory

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3 2 1
```

**Output**:
```
2
```

### Example 2

**Input**:
```
3 2 2
```

**Output**:
```
4
```

### Example 3

**Input**:
```
4 2 2
```

**Output**:
```
4
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
