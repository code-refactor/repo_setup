# 846_E. Chemistry in Berland

**ID:** 846_e_chemistry_in_berland_60
**Difficulty:** 11

## Description

Igor is a post-graduate student of chemistry faculty in Berland State University (BerSU). He needs to conduct a complicated experiment to write his thesis, but laboratory of BerSU doesn't contain all the materials required for this experiment.

Fortunately, chemical laws allow material transformations (yes, chemistry in Berland differs from ours). But the rules of transformation are a bit strange.

Berland chemists are aware of n materials, numbered in the order they were discovered. Each material can be transformed into some other material (or vice versa). Formally, for each i (2 ≤ i ≤ n) there exist two numbers xi and ki that denote a possible transformation: ki kilograms of material xi can be transformed into 1 kilogram of material i, and 1 kilogram of material i can be transformed into 1 kilogram of material xi. Chemical processing equipment in BerSU allows only such transformation that the amount of resulting material is always an integer number of kilograms.

For each i (1 ≤ i ≤ n) Igor knows that the experiment requires ai kilograms of material i, and the laboratory contains bi kilograms of this material. Is it possible to conduct an experiment after transforming some materials (or none)?

Input

The first line contains one integer number n (1 ≤ n ≤ 105) — the number of materials discovered by Berland chemists.

The second line contains n integer numbers b1, b2... bn (1 ≤ bi ≤ 1012) — supplies of BerSU laboratory.

The third line contains n integer numbers a1, a2... an (1 ≤ ai ≤ 1012) — the amounts required for the experiment.

Then n - 1 lines follow. j-th of them contains two numbers xj + 1 and kj + 1 that denote transformation of (j + 1)-th material (1 ≤ xj + 1 ≤ j, 1 ≤ kj + 1 ≤ 109).

Output

Print YES if it is possible to conduct an experiment. Otherwise print NO.

Examples

Input

3
1 2 3
3 2 1
1 1
1 1


Output

YES


Input

3
3 2 1
1 2 3
1 1
1 2


Output

NO

## Categories

- dfs and similar
- greedy
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3
3 2 1
1 2 3
1 1
1 2
```

**Output**:
```
NO
```

### Example 2

**Input**:
```
3
1 2 3
3 2 1
1 1
1 1
```

**Output**:
```
YES
```

### Example 3

**Input**:
```
5
27468 7465 74275 40573 40155
112071 76270 244461 264202 132397
1 777133331
2 107454154
3 652330694
4 792720519
```

**Output**:
```
NO
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
