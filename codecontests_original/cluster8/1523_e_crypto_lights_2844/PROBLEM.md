# 1523_E. Crypto Lights

**ID:** 1523_e_crypto_lights_2844
**Difficulty:** 11

## Description

<image>

To monitor cryptocurrency exchange rates trader William invented a wonderful device consisting of n lights arranged in a row. The device functions in the following way:

Initially, all lights on William's device are turned off. At the beginning of a new iteration the device randomly, with a uniform distribution, picks a light that is turned off and turns it on, telling William which cryptocurrency he should invest in. After this iteration if any k consecutive lights contain more than one turned on light, then the device finishes working.

William doesn't like uncertainty, so he wants you to calculate the expected value of the number of lights that are turned on in the device after it finishes working.

Input

Each test contains multiple test cases. The first line contains the number of test cases t (1 ≤ t ≤ 10). Description of the test cases follows.

The only line for each test case contains two integers n and k (2 ≤ k ≤ n ≤ 10^5), which are the total number of lights and the length of subsegment of lights that are being checked, respectively.

Output

For each test case print the answer, modulo 10^9+7. 

Formally, let M = 10^9+7. It can be shown that the answer can be expressed as an irreducible fraction p/q, where p and q are integers and q not ≡ 0 \pmod{M}. Output the integer equal to p ⋅ q^{-1} mod M. In other words, output such an integer x that 0 ≤ x < M and x ⋅ q ≡ p \pmod{M}.

Example

Input


3
3 2
15 2
40 15


Output


333333338
141946947
329622137

Note

Explanation of the first sample test case:

Let's write out all possible sequences of light toggles, which will make the device complete its operation:

  1. (1, 2) — 2 lights are turned on 
  2. (1, 3, 2) — 3 lights are turned on 
  3. (2, 1) — 2 lights are turned on 
  4. (2, 3) — 2 lights are turned on 
  5. (3, 2) — 2 lights are turned on 
  6. (3, 1, 2) — 3 lights are turned on 



Then the final expected value will be equal to 2/6 + 3/6 + 2/6 + 2/6 + 2/6 + 3/6 = 14/6 = 7/3. 

Then the required output will be 333333338, since 333333338 ⋅ 3 ≡ 7 \pmod{10^9+7}.

## Categories

- combinatorics
- dp
- math
- probabilities

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3
3 2
15 2
40 15
```

**Output**:
```
333333338
141946947
329622137
```

### Example 2

**Input**:
```
10
100000 99995
100000 100000
100000 99998
100000 99997
100000 99997
100000 99997
100000 100000
100000 99997
100000 99999
100000 99998
```

**Output**:
```
537223949
2
907444797
814889585
814889585
814889585
2
814889585
635814936
907444797
```

### Example 3

**Input**:
```
10
91147 3
60637 60633
58274 58270
81624 62
59542 17
76280 76277
78239 3
84713 84710
58143 58143
85720 5
```

**Output**:
```
623680566
119279988
824480296
763186315
30533224
302872289
396710457
752099342
2
175711061
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
