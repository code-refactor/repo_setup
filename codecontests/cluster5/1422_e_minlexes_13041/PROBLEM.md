# 1422_E. Minlexes

**ID:** 1422_e_minlexes_13041
**Difficulty:** 11

## Description

Some time ago Lesha found an entertaining string s consisting of lowercase English letters. Lesha immediately developed an unique algorithm for this string and shared it with you. The algorithm is as follows.

Lesha chooses an arbitrary (possibly zero) number of pairs on positions (i, i + 1) in such a way that the following conditions are satisfied: 

  * for each pair (i, i + 1) the inequality 0 ≤ i < |s| - 1 holds; 
  * for each pair (i, i + 1) the equality s_i = s_{i + 1} holds; 
  * there is no index that is contained in more than one pair. 

After that Lesha removes all characters on indexes contained in these pairs and the algorithm is over. 

Lesha is interested in the lexicographically smallest strings he can obtain by applying the algorithm to the suffixes of the given string.

Input

The only line contains the string s (1 ≤ |s| ≤ 10^5) — the initial string consisting of lowercase English letters only.

Output

In |s| lines print the lengths of the answers and the answers themselves, starting with the answer for the longest suffix. The output can be large, so, when some answer is longer than 10 characters, instead print the first 5 characters, then "...", then the last 2 characters of the answer.

Examples

Input


abcdd


Output


3 abc
2 bc
1 c
0 
1 d


Input


abbcdddeaaffdfouurtytwoo


Output


18 abbcd...tw
17 bbcdd...tw
16 bcddd...tw
15 cddde...tw
14 dddea...tw
13 ddeaa...tw
12 deaad...tw
11 eaadf...tw
10 aadfortytw
9 adfortytw
8 dfortytw
9 fdfortytw
8 dfortytw
7 fortytw
6 ortytw
5 rtytw
6 urtytw
5 rtytw
4 tytw
3 ytw
2 tw
1 w
0 
1 o

Note

Consider the first example.

  * The longest suffix is the whole string "abcdd". Choosing one pair (4, 5), Lesha obtains "abc". 
  * The next longest suffix is "bcdd". Choosing one pair (3, 4), we obtain "bc". 
  * The next longest suffix is "cdd". Choosing one pair (2, 3), we obtain "c". 
  * The next longest suffix is "dd". Choosing one pair (1, 2), we obtain "" (an empty string). 
  * The last suffix is the string "d". No pair can be chosen, so the answer is "d". 



In the second example, for the longest suffix "abbcdddeaaffdfouurtytwoo" choose three pairs (11, 12), (16, 17), (23, 24) and we obtain "abbcdddeaadfortytw"

## Categories

- dp
- greedy
- implementation
- strings

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
abcdd
```

**Output**:
```
3 abc
2 bc
1 c
0 
1 d
```

### Example 2

**Input**:
```
abbcdddeaaffdfouurtytwoo
```

**Output**:
```
18 abbcd...tw
17 bbcdd...tw
16 bcddd...tw
15 cddde...tw
14 dddea...tw
13 ddeaa...tw
12 deaad...tw
11 eaadf...tw
10 aadfortytw
9 adfortytw
8 dfortytw
9 fdfortytw
8 dfortytw
7 fortytw
6 ortytw
5 rtytw
6 urtytw
5 rtytw
4 tytw
3 ytw
2 tw
1 w
0 
1 o
```

### Example 3

**Input**:
```
nnnnnnnnnnnnnnnnaaag
```

**Output**:
```
4 aaag
5 naaag
4 aaag
5 naaag
4 aaag
5 naaag
4 aaag
5 naaag
4 aaag
5 naaag
4 aaag
5 naaag
4 aaag
5 naaag
4 aaag
5 naaag
4 aaag
3 aag
2 ag
1 g
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
