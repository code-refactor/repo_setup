# 1543_C. Need for Pink Slips

**ID:** 1543_c_need_for_pink_slips_3469
**Difficulty:** 9

## Description

After defeating a Blacklist Rival, you get a chance to draw 1 reward slip out of x hidden valid slips. Initially, x=3 and these hidden valid slips are Cash Slip, Impound Strike Release Marker and Pink Slip of Rival's Car. Initially, the probability of drawing these in a random guess are c, m, and p, respectively. There is also a volatility factor v. You can play any number of Rival Races as long as you don't draw a Pink Slip. Assume that you win each race and get a chance to draw a reward slip. In each draw, you draw one of the x valid items with their respective probabilities. Suppose you draw a particular item and its probability of drawing before the draw was a. Then,

  * If the item was a Pink Slip, the quest is over, and you will not play any more races. 
  * Otherwise, 
    1. If a≤ v, the probability of the item drawn becomes 0 and the item is no longer a valid item for all the further draws, reducing x by 1. Moreover, the reduced probability a is distributed equally among the other remaining valid items. 
    2. If a > v, the probability of the item drawn reduces by v and the reduced probability is distributed equally among the other valid items. 



For example,

  * If (c,m,p)=(0.2,0.1,0.7) and v=0.1, after drawing Cash, the new probabilities will be (0.1,0.15,0.75). 
  * If (c,m,p)=(0.1,0.2,0.7) and v=0.2, after drawing Cash, the new probabilities will be (Invalid,0.25,0.75). 
  * If (c,m,p)=(0.2,Invalid,0.8) and v=0.1, after drawing Cash, the new probabilities will be (0.1,Invalid,0.9). 
  * If (c,m,p)=(0.1,Invalid,0.9) and v=0.2, after drawing Cash, the new probabilities will be (Invalid,Invalid,1.0). 



You need the cars of Rivals. So, you need to find the expected number of races that you must play in order to draw a pink slip.

Input

The first line of input contains a single integer t (1≤ t≤ 10) — the number of test cases.

The first and the only line of each test case contains four real numbers c, m, p and v (0 < c,m,p < 1, c+m+p=1, 0.1≤ v≤ 0.9).

Additionally, it is guaranteed that each of c, m, p and v have at most 4 decimal places.

Output

For each test case, output a single line containing a single real number — the expected number of races that you must play in order to draw a Pink Slip.

Your answer is considered correct if its absolute or relative error does not exceed 10^{-6}.

Formally, let your answer be a, and the jury's answer be b. Your answer is accepted if and only if \frac{|a - b|}{max{(1, |b|)}} ≤ 10^{-6}.

Example

Input


4
0.2 0.2 0.6 0.2
0.4 0.2 0.4 0.8
0.4998 0.4998 0.0004 0.1666
0.3125 0.6561 0.0314 0.2048


Output


1.532000000000
1.860000000000
5.005050776521
4.260163673896

Note

For the first test case, the possible drawing sequences are: 

  * P with a probability of 0.6; 
  * CP with a probability of 0.2⋅ 0.7 = 0.14; 
  * CMP with a probability of 0.2⋅ 0.3⋅ 0.9 = 0.054; 
  * CMMP with a probability of 0.2⋅ 0.3⋅ 0.1⋅ 1 = 0.006; 
  * MP with a probability of 0.2⋅ 0.7 = 0.14; 
  * MCP with a probability of 0.2⋅ 0.3⋅ 0.9 = 0.054; 
  * MCCP with a probability of 0.2⋅ 0.3⋅ 0.1⋅ 1 = 0.006. 

So, the expected number of races is equal to 1⋅ 0.6 + 2⋅ 0.14 + 3⋅ 0.054 + 4⋅ 0.006 + 2⋅ 0.14 + 3⋅ 0.054 + 4⋅ 0.006 = 1.532.

For the second test case, the possible drawing sequences are: 

  * P with a probability of 0.4; 
  * CP with a probability of 0.4⋅ 0.6 = 0.24; 
  * CMP with a probability of 0.4⋅ 0.4⋅ 1 = 0.16; 
  * MP with a probability of 0.2⋅ 0.5 = 0.1; 
  * MCP with a probability of 0.2⋅ 0.5⋅ 1 = 0.1. 



So, the expected number of races is equal to 1⋅ 0.4 + 2⋅ 0.24 + 3⋅ 0.16 + 2⋅ 0.1 + 3⋅ 0.1 = 1.86.

## Categories

- bitmasks
- brute force
- dfs and similar
- implementation
- math
- probabilities

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
4
0.2 0.2 0.6 0.2
0.4 0.2 0.4 0.8
0.4998 0.4998 0.0004 0.1666
0.3125 0.6561 0.0314 0.2048
```

**Output**:
```
1.53200000000000002842
1.86000000000000031974
5.00505077652118934850
4.26016367389582129022
```

### Example 2

**Input**:
```
10
0.1816 0.7813 0.0371 0.6860
0.4789 0.1463 0.3748 0.6186
0.1431 0.3218 0.5351 0.6905
0.7071 0.0774 0.2155 0.1087
0.7082 0.0144 0.2774 0.7364
0.0824 0.4306 0.4870 0.5198
0.2039 0.7827 0.0134 0.3187
0.2667 0.5149 0.2184 0.7938
0.6990 0.2677 0.0333 0.3471
0.3924 0.5833 0.0243 0.4838
```

**Output**:
```
2.82425254469650033329
1.89070059000000001426
1.61901558500000009033
3.22301388833152913094
1.99387346000000031943
1.68006593999999997990
3.68630126561879967184
2.22437310999999970917
3.41825818584635054975
3.09346908695883104912
```

### Example 3

**Input**:
```
10
0.5417 0.3601 0.0982 0.1086
0.5651 0.0015 0.4334 0.1310
0.6241 0.0182 0.3577 0.1915
0.3619 0.4496 0.1885 0.1625
0.0894 0.1814 0.7292 0.1540
0.7853 0.1498 0.0649 0.1417
0.9355 0.0597 0.0048 0.1810
0.9060 0.0888 0.0052 0.1004
0.0523 0.4169 0.5308 0.1969
0.9919 0.0024 0.0057 0.1176
```

**Output**:
```
4.43232336497016632393
2.03806293676083827293
2.22627888042582400274
3.17204317134115854060
1.33231514217809232647
4.46909397903456895307
4.71374200641801532896
6.05744576510617260823
1.70334021728854789757
5.71408133564027931328
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
