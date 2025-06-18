# 167_B. Wizards and Huge Prize

**ID:** 167_b_wizards_and_huge_prize_1597
**Difficulty:** 8

## Description

One must train much to do well on wizardry contests. So, there are numerous wizardry schools and magic fees.

One of such magic schools consists of n tours. A winner of each tour gets a huge prize. The school is organised quite far away, so one will have to take all the prizes home in one go. And the bags that you've brought with you have space for no more than k huge prizes.

Besides the fact that you want to take all the prizes home, you also want to perform well. You will consider your performance good if you win at least l tours.

In fact, years of organizing contests proved to the organizers that transporting huge prizes is an issue for the participants. Alas, no one has ever invented a spell that would shrink the prizes... So, here's the solution: for some tours the winner gets a bag instead of a huge prize. Each bag is characterized by number ai — the number of huge prizes that will fit into it.

You already know the subject of all tours, so you can estimate the probability pi of winning the i-th tour. You cannot skip the tour under any circumstances.

Find the probability that you will perform well on the contest and will be able to take all won prizes home (that is, that you will be able to fit all the huge prizes that you won into the bags that you either won or brought from home).

Input

The first line contains three integers n, l, k (1 ≤ n ≤ 200, 0 ≤ l, k ≤ 200) — the number of tours, the minimum number of tours to win, and the number of prizes that you can fit in the bags brought from home, correspondingly.

The second line contains n space-separated integers, pi (0 ≤ pi ≤ 100) — the probability to win the i-th tour, in percents.

The third line contains n space-separated integers, ai (1 ≤ ai ≤ 200) — the capacity of the bag that will be awarded to you for winning the i-th tour, or else -1, if the prize for the i-th tour is a huge prize and not a bag.

Output

Print a single real number — the answer to the problem. The answer will be accepted if the absolute or relative error does not exceed 10 - 6.

Examples

Input

3 1 0
10 20 30
-1 -1 2


Output

0.300000000000


Input

1 1 1
100
123


Output

1.000000000000

Note

In the first sample we need either win no tour or win the third one. If we win nothing we wouldn't perform well. So, we must to win the third tour. Other conditions will be satisfied in this case. Probability of wining the third tour is 0.3.

In the second sample we win the only tour with probability 1.0, and go back home with bag for it.

## Categories

- dp
- math
- probabilities

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3 1 0
10 20 30
-1 -1 2
```

**Output**:
```
0.3000000
```

### Example 2

**Input**:
```
1 1 1
100
123
```

**Output**:
```
1.0000000
```

### Example 3

**Input**:
```
17 5 17
69 43 30 9 17 75 43 42 3 10 47 90 82 47 1 51 31
-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
```

**Output**:
```
0.9242231
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
