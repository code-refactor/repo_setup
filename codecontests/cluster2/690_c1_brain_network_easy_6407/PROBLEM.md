# 690_C1. Brain Network (easy)

**ID:** 690_c1_brain_network_easy_6407
**Difficulty:** 9

## Description

One particularly well-known fact about zombies is that they move and think terribly slowly. While we still don't know why their movements are so sluggish, the problem of laggy thinking has been recently resolved. It turns out that the reason is not (as previously suspected) any kind of brain defect – it's the opposite! Independent researchers confirmed that the nervous system of a zombie is highly complicated – it consists of n brains (much like a cow has several stomachs). They are interconnected by brain connectors, which are veins capable of transmitting thoughts between brains. There are two important properties such a brain network should have to function properly: 

  1. It should be possible to exchange thoughts between any two pairs of brains (perhaps indirectly, through other brains). 
  2. There should be no redundant brain connectors, that is, removing any brain connector would make property 1 false. 



If both properties are satisfied, we say that the nervous system is valid. Unfortunately (?), if the system is not valid, the zombie stops thinking and becomes (even more) dead. Your task is to analyze a given nervous system of a zombie and find out whether it is valid.

Input

The first line of the input contains two space-separated integers n and m (1 ≤ n, m ≤ 1000) denoting the number of brains (which are conveniently numbered from 1 to n) and the number of brain connectors in the nervous system, respectively. In the next m lines, descriptions of brain connectors follow. Every connector is given as a pair of brains a b it connects (1 ≤ a, b ≤ n, a ≠ b).

Output

The output consists of one line, containing either yes or no depending on whether the nervous system is valid.

Examples

Input

4 4
1 2
2 3
3 1
4 1


Output

no


Input

6 5
1 2
2 3
3 4
4 5
3 6


Output

yes


## Source

Codeforces

## Examples

### Example 1

**Input**:
```
6 5
1 2
2 3
3 4
4 5
3 6
```

**Output**:
```
yes
```

### Example 2

**Input**:
```
4 4
1 2
2 3
3 1
4 1
```

**Output**:
```
no
```

### Example 3

**Input**:
```
10 9
2 3
6 8
10 1
1 8
6 7
8 7
10 5
7 10
2 5
```

**Output**:
```
no
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
