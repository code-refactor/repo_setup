# 1303_E. Erase Subsequences

**ID:** 1303_e_erase_subsequences_10330
**Difficulty:** 11

## Description

You are given a string s. You can build new string p from s using the following operation no more than two times: 

  1. choose any subsequence s_{i_1}, s_{i_2}, ..., s_{i_k} where 1 ≤ i_1 < i_2 < ... < i_k ≤ |s|; 
  2. erase the chosen subsequence from s (s can become empty); 
  3. concatenate chosen subsequence to the right of the string p (in other words, p = p + s_{i_1}s_{i_2}... s_{i_k}). 



Of course, initially the string p is empty. 

For example, let s = ababcd. At first, let's choose subsequence s_1 s_4 s_5 = abc — we will get s = bad and p = abc. At second, let's choose s_1 s_2 = ba — we will get s = d and p = abcba. So we can build abcba from ababcd.

Can you build a given string t using the algorithm above?

Input

The first line contains the single integer T (1 ≤ T ≤ 100) — the number of test cases.

Next 2T lines contain test cases — two per test case. The first line contains string s consisting of lowercase Latin letters (1 ≤ |s| ≤ 400) — the initial string.

The second line contains string t consisting of lowercase Latin letters (1 ≤ |t| ≤ |s|) — the string you'd like to build.

It's guaranteed that the total length of strings s doesn't exceed 400.

Output

Print T answers — one per test case. Print YES (case insensitive) if it's possible to build t and NO (case insensitive) otherwise.

Example

Input


4
ababcd
abcba
a
b
defi
fed
xyz
x


Output


YES
NO
NO
YES

## Categories

- dp
- strings

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
4
ababcd
abcba
a
b
defi
fed
xyz
x
```

**Output**:
```
YES
NO
NO
YES
```

### Example 2

**Input**:
```
3
ababc
abcba
feded
defed
ababcfeded
abcdebafed
```

**Output**:
```
YES
YES
YES
```

### Example 3

**Input**:
```
1
bbbaaaaabbabaabbbbaabbbbabbaabbaababbbbbbababbababbbaaaaaaabaababbbaababbbbababbbabbbbbabaabbaaaabaa
bbbababbaabbbbbaabaaabaababaaaabaabbbabbababaaabba
```

**Output**:
```
YES
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
