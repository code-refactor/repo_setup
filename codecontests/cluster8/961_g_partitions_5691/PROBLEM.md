# 961_G. Partitions

**ID:** 961_g_partitions_5691
**Difficulty:** 13

## Description

You are given a set of n elements indexed from 1 to n. The weight of i-th element is wi. The weight of some subset of a given set is denoted as <image>. The weight of some partition R of a given set into k subsets is <image> (recall that a partition of a given set is a set of its subsets such that every element of the given set belongs to exactly one subset in partition).

Calculate the sum of weights of all partitions of a given set into exactly k non-empty subsets, and print it modulo 109 + 7. Two partitions are considered different iff there exist two elements x and y such that they belong to the same set in one of the partitions, and to different sets in another partition.

Input

The first line contains two integers n and k (1 ≤ k ≤ n ≤ 2·105) — the number of elements and the number of subsets in each partition, respectively.

The second line contains n integers wi (1 ≤ wi ≤ 109)— weights of elements of the set.

Output

Print one integer — the sum of weights of all partitions of a given set into k non-empty subsets, taken modulo 109 + 7.

Examples

Input

4 2
2 3 2 3


Output

160


Input

5 2
1 2 3 4 5


Output

645

Note

Possible partitions in the first sample:

  1. {{1, 2, 3}, {4}}, W(R) = 3·(w1 + w2 + w3) + 1·w4 = 24; 
  2. {{1, 2, 4}, {3}}, W(R) = 26; 
  3. {{1, 3, 4}, {2}}, W(R) = 24; 
  4. {{1, 2}, {3, 4}}, W(R) = 2·(w1 + w2) + 2·(w3 + w4) = 20; 
  5. {{1, 3}, {2, 4}}, W(R) = 20; 
  6. {{1, 4}, {2, 3}}, W(R) = 20; 
  7. {{1}, {2, 3, 4}}, W(R) = 26; 



Possible partitions in the second sample:

  1. {{1, 2, 3, 4}, {5}}, W(R) = 45; 
  2. {{1, 2, 3, 5}, {4}}, W(R) = 48; 
  3. {{1, 2, 4, 5}, {3}}, W(R) = 51; 
  4. {{1, 3, 4, 5}, {2}}, W(R) = 54; 
  5. {{2, 3, 4, 5}, {1}}, W(R) = 57; 
  6. {{1, 2, 3}, {4, 5}}, W(R) = 36; 
  7. {{1, 2, 4}, {3, 5}}, W(R) = 37; 
  8. {{1, 2, 5}, {3, 4}}, W(R) = 38; 
  9. {{1, 3, 4}, {2, 5}}, W(R) = 38; 
  10. {{1, 3, 5}, {2, 4}}, W(R) = 39; 
  11. {{1, 4, 5}, {2, 3}}, W(R) = 40; 
  12. {{2, 3, 4}, {1, 5}}, W(R) = 39; 
  13. {{2, 3, 5}, {1, 4}}, W(R) = 40; 
  14. {{2, 4, 5}, {1, 3}}, W(R) = 41; 
  15. {{3, 4, 5}, {1, 2}}, W(R) = 42. 

## Categories

- combinatorics
- math
- number theory

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5 2
1 2 3 4 5
```

**Output**:
```
645
```

### Example 2

**Input**:
```
4 2
2 3 2 3
```

**Output**:
```
160
```

### Example 3

**Input**:
```
5 2
3113 612 440 2761 6970
```

**Output**:
```
597528
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
