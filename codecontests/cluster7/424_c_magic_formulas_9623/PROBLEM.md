# 424_C. Magic Formulas

**ID:** 424_c_magic_formulas_9623
**Difficulty:** 9

## Description

People in the Tomskaya region like magic formulas very much. You can see some of them below.

Imagine you are given a sequence of positive integer numbers p1, p2, ..., pn. Lets write down some magic formulas:

<image><image>

Here, "mod" means the operation of taking the residue after dividing.

The expression <image> means applying the bitwise xor (excluding "OR") operation to integers x and y. The given operation exists in all modern programming languages. For example, in languages C++ and Java it is represented by "^", in Pascal — by "xor".

People in the Tomskaya region like magic formulas very much, but they don't like to calculate them! Therefore you are given the sequence p, calculate the value of Q.

Input

The first line of the input contains the only integer n (1 ≤ n ≤ 106). The next line contains n integers: p1, p2, ..., pn (0 ≤ pi ≤ 2·109).

Output

The only line of output should contain a single integer — the value of Q.

Examples

Input

3
1 2 3


Output

3

## Categories

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
3
```

### Example 2

**Input**:
```
20
1999581813 313463235 1733614990 662007911 1789348031 1120800519 196972430 1579897311 191001928 241720485 1426288783 1103088596 839698523 1974815116 77040208 904949865 840522850 1488919296 1027394709 857931762
```

**Output**:
```
1536068328
```

### Example 3

**Input**:
```
25
39226529 640445129 936289624 364461191 1096077769 573427707 1919403410 950067229 1217479531 455229458 1574949468 397268319 1267289585 995220637 1920919164 501015483 1815262670 1197059269 86947741 1137410885 667368575 733666398 1536581408 611239452 947487746
```

**Output**:
```
259654661
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
