# 126_B. Password

**ID:** 126_b_password_13138
**Difficulty:** 8

## Description

Asterix, Obelix and their temporary buddies Suffix and Prefix has finally found the Harmony temple. However, its doors were firmly locked and even Obelix had no luck opening them.

A little later they found a string s, carved on a rock below the temple's gates. Asterix supposed that that's the password that opens the temple and read the string aloud. However, nothing happened. Then Asterix supposed that a password is some substring t of the string s.

Prefix supposed that the substring t is the beginning of the string s; Suffix supposed that the substring t should be the end of the string s; and Obelix supposed that t should be located somewhere inside the string s, that is, t is neither its beginning, nor its end.

Asterix chose the substring t so as to please all his companions. Besides, from all acceptable variants Asterix chose the longest one (as Asterix loves long strings). When Asterix read the substring t aloud, the temple doors opened. 

You know the string s. Find the substring t or determine that such substring does not exist and all that's been written above is just a nice legend.

Input

You are given the string s whose length can vary from 1 to 106 (inclusive), consisting of small Latin letters.

Output

Print the string t. If a suitable t string does not exist, then print "Just a legend" without the quotes.

Examples

Input

fixprefixsuffix


Output

fix

Input

abcdabc


Output

Just a legend

## Categories

- binary search
- dp
- hashing
- string suffix structures
- strings

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
abcdabc
```

**Output**:
```
Just a legend
```

### Example 2

**Input**:
```
fixprefixsuffix
```

**Output**:
```
fix
```

### Example 3

**Input**:
```
aaabaabaaaaab
```

**Output**:
```
Just a legend
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
