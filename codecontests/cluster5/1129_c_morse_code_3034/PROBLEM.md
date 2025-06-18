# 1129_C. Morse Code

**ID:** 1129_c_morse_code_3034
**Difficulty:** 9

## Description

In Morse code, an letter of English alphabet is represented as a string of some length from 1 to 4. Moreover, each Morse code representation of an English letter contains only dots and dashes. In this task, we will represent a dot with a "0" and a dash with a "1".

Because there are 2^1+2^2+2^3+2^4 = 30 strings with length 1 to 4 containing only "0" and/or "1", not all of them correspond to one of the 26 English letters. In particular, each string of "0" and/or "1" of length at most 4 translates into a distinct English letter, except the following four strings that do not correspond to any English alphabet: "0011", "0101", "1110", and "1111".

You will work with a string S, which is initially empty. For m times, either a dot or a dash will be appended to S, one at a time. Your task is to find and report, after each of these modifications to string S, the number of non-empty sequences of English letters that are represented with some substring of S in Morse code.

Since the answers can be incredibly tremendous, print them modulo 10^9 + 7.

Input

The first line contains an integer m (1 ≤ m ≤ 3 000) — the number of modifications to S. 

Each of the next m lines contains either a "0" (representing a dot) or a "1" (representing a dash), specifying which character should be appended to S.

Output

Print m lines, the i-th of which being the answer after the i-th modification to S.

Examples

Input

3
1
1
1


Output

1
3
7


Input

5
1
0
1
0
1


Output

1
4
10
22
43


Input

9
1
1
0
0
0
1
1
0
1


Output

1
3
10
24
51
109
213
421
833

Note

Let us consider the first sample after all characters have been appended to S, so S is "111".

As you can see, "1", "11", and "111" all correspond to some distinct English letter. In fact, they are translated into a 'T', an 'M', and an 'O', respectively. All non-empty sequences of English letters that are represented with some substring of S in Morse code, therefore, are as follows.

  1. "T" (translates into "1") 
  2. "M" (translates into "11") 
  3. "O" (translates into "111") 
  4. "TT" (translates into "11") 
  5. "TM" (translates into "111") 
  6. "MT" (translates into "111") 
  7. "TTT" (translates into "111") 



Although unnecessary for this task, a conversion table from English alphabets into Morse code can be found [here](https://en.wikipedia.org/wiki/Morse_code).

## Categories

- binary search
- data structures
- dp
- hashing
- sortings
- string suffix structures
- strings

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5
1
0
1
0
1
```

**Output**:
```
1
4
10
22
43
```

### Example 2

**Input**:
```
9
1
1
0
0
0
1
1
0
1
```

**Output**:
```
1
3
10
24
51
109
213
421
833
```

### Example 3

**Input**:
```
3
1
1
1
```

**Output**:
```
1
3
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