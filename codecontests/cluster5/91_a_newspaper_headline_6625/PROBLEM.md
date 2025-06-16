# 91_A. Newspaper Headline

**ID:** 91_a_newspaper_headline_6625
**Difficulty:** very hard

## Description

A newspaper is published in Walrusland. Its heading is s1, it consists of lowercase Latin letters. Fangy the little walrus wants to buy several such newspapers, cut out their headings, glue them one to another in order to get one big string. After that walrus erase several letters from this string in order to get a new word s2. It is considered that when Fangy erases some letter, there's no whitespace formed instead of the letter. That is, the string remains unbroken and it still only consists of lowercase Latin letters.

For example, the heading is "abc". If we take two such headings and glue them one to the other one, we get "abcabc". If we erase the letters on positions 1 and 5, we get a word "bcac".

Which least number of newspaper headings s1 will Fangy need to glue them, erase several letters and get word s2?

Input

The input data contain two lines. The first line contain the heading s1, the second line contains the word s2. The lines only consist of lowercase Latin letters (1 ≤ |s1| ≤ 104, 1 ≤ |s2| ≤ 106).

Output

If it is impossible to get the word s2 in the above-described manner, print "-1" (without the quotes). Otherwise, print the least number of newspaper headings s1, which Fangy will need to receive the word s2.

Examples

Input

abc
xyz


Output

-1


Input

abcd
dabc


Output

2

## Categories

- greedy
- strings

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
abc
xyz
```

**Output**:
```
-1
```

### Example 2

**Input**:
```
abcd
dabc
```

**Output**:
```
2
```

### Example 3

**Input**:
```
fcagdciidcedeaicgfffgjefaefaachfbfj
aiecchjehdgbjfcdjdefgfhiddjajeddiigidaibejabd
```

**Output**:
```
11
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
