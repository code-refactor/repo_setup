# 653_B. Bear and Compressing

**ID:** 653_b_bear_and_compressing_5990
**Difficulty:** 8

## Description

Limak is a little polar bear. Polar bears hate long strings and thus they like to compress them. You should also know that Limak is so young that he knows only first six letters of the English alphabet: 'a', 'b', 'c', 'd', 'e' and 'f'.

You are given a set of q possible operations. Limak can perform them in any order, any operation may be applied any number of times. The i-th operation is described by a string ai of length two and a string bi of length one. No two of q possible operations have the same string ai.

When Limak has a string s he can perform the i-th operation on s if the first two letters of s match a two-letter string ai. Performing the i-th operation removes first two letters of s and inserts there a string bi. See the notes section for further clarification.

You may note that performing an operation decreases the length of a string s exactly by 1. Also, for some sets of operations there may be a string that cannot be compressed any further, because the first two letters don't match any ai.

Limak wants to start with a string of length n and perform n - 1 operations to finally get a one-letter string "a". In how many ways can he choose the starting string to be able to get "a"? Remember that Limak can use only letters he knows.

Input

The first line contains two integers n and q (2 ≤ n ≤ 6, 1 ≤ q ≤ 36) — the length of the initial string and the number of available operations.

The next q lines describe the possible operations. The i-th of them contains two strings ai and bi (|ai| = 2, |bi| = 1). It's guaranteed that ai ≠ aj for i ≠ j and that all ai and bi consist of only first six lowercase English letters.

Output

Print the number of strings of length n that Limak will be able to transform to string "a" by applying only operations given in the input.

Examples

Input

3 5
ab a
cc c
ca a
ee c
ff d


Output

4


Input

2 8
af e
dc d
cc f
bc b
da b
eb a
bb b
ff c


Output

1


Input

6 2
bb a
ba a


Output

0

Note

In the first sample, we count initial strings of length 3 from which Limak can get a required string "a". There are 4 such strings: "abb", "cab", "cca", "eea". The first one Limak can compress using operation 1 two times (changing "ab" to a single "a"). The first operation would change "abb" to "ab" and the second operation would change "ab" to "a".

Other three strings may be compressed as follows: 

  * "cab" <image> "ab" <image> "a" 
  * "cca" <image> "ca" <image> "a" 
  * "eea" <image> "ca" <image> "a" 



In the second sample, the only correct initial string is "eb" because it can be immediately compressed to "a".

## Categories

- brute force
- dfs and similar
- dp
- strings

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
6 2
bb a
ba a
```

**Output**:
```
0
```

### Example 2

**Input**:
```
2 8
af e
dc d
cc f
bc b
da b
eb a
bb b
ff c
```

**Output**:
```
1
```

### Example 3

**Input**:
```
3 5
ab a
cc c
ca a
ee c
ff d
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
