# 925_C. Big Secret

**ID:** 925_c_big_secret_3711
**Difficulty:** 9

## Description

Vitya has learned that the answer for The Ultimate Question of Life, the Universe, and Everything is not the integer 54 42, but an increasing integer sequence a_1, …, a_n. In order to not reveal the secret earlier than needed, Vitya encrypted the answer and obtained the sequence b_1, …, b_n using the following rules:

  * b_1 = a_1;
  * b_i = a_i ⊕ a_{i - 1} for all i from 2 to n, where x ⊕ y is the [bitwise XOR](https://en.wikipedia.org/wiki/Bitwise_operation#XOR) of x and y. 



It is easy to see that the original sequence can be obtained using the rule a_i = b_1 ⊕ … ⊕ b_i.

However, some time later Vitya discovered that the integers b_i in the cypher got shuffled, and it can happen that when decrypted using the rule mentioned above, it can produce a sequence that is not increasing. In order to save his reputation in the scientific community, Vasya decided to find some permutation of integers b_i so that the sequence a_i = b_1 ⊕ … ⊕ b_i is strictly increasing. Help him find such a permutation or determine that it is impossible.

Input

The first line contains a single integer n (1 ≤ n ≤ 10^5).

The second line contains n integers b_1, …, b_n (1 ≤ b_i < 2^{60}).

Output

If there are no valid permutations, print a single line containing "No".

Otherwise in the first line print the word "Yes", and in the second line print integers b'_1, …, b'_n — a valid permutation of integers b_i. The unordered multisets \\{b_1, …, b_n\} and \\{b'_1, …, b'_n\} should be equal, i. e. for each integer x the number of occurrences of x in the first multiset should be equal to the number of occurrences of x in the second multiset. Apart from this, the sequence a_i = b'_1 ⊕ … ⊕ b'_i should be strictly increasing.

If there are multiple answers, print any of them.

Examples

Input

3
1 2 3


Output

No


Input

6
4 7 7 12 31 61


Output

Yes
4 12 7 31 7 61 

Note

In the first example no permutation is valid.

In the second example the given answer lead to the sequence a_1 = 4, a_2 = 8, a_3 = 15, a_4 = 16, a_5 = 23, a_6 = 42.

## Categories

- constructive algorithms
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3
1 2 3
```

**Output**:
```
No
```

### Example 2

**Input**:
```
6
4 7 7 12 31 61
```

**Output**:
```
Yes
4 12 7 31 7 61
```

### Example 3

**Input**:
```
1
4
```

**Output**:
```
Yes
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
