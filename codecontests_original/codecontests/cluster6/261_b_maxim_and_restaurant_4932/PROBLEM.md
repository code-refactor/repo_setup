# 261_B. Maxim and Restaurant

**ID:** 261_b_maxim_and_restaurant_4932
**Difficulty:** 8

## Description

Maxim has opened his own restaurant! The restaurant has got a huge table, the table's length is p meters.

Maxim has got a dinner party tonight, n guests will come to him. Let's index the guests of Maxim's restaurant from 1 to n. Maxim knows the sizes of all guests that are going to come to him. The i-th guest's size (ai) represents the number of meters the guest is going to take up if he sits at the restaurant table.

Long before the dinner, the guests line up in a queue in front of the restaurant in some order. Then Maxim lets the guests in, one by one. Maxim stops letting the guests in when there is no place at the restaurant table for another guest in the queue. There is no place at the restaurant table for another guest in the queue, if the sum of sizes of all guests in the restaurant plus the size of this guest from the queue is larger than p. In this case, not to offend the guest who has no place at the table, Maxim doesn't let any other guest in the restaurant, even if one of the following guests in the queue would have fit in at the table.

Maxim is now wondering, what is the average number of visitors who have come to the restaurant for all possible n! orders of guests in the queue. Help Maxim, calculate this number.

Input

The first line contains integer n (1 ≤ n ≤ 50) — the number of guests in the restaurant. The next line contains integers a1, a2, ..., an (1 ≤ ai ≤ 50) — the guests' sizes in meters. The third line contains integer p (1 ≤ p ≤ 50) — the table's length in meters. 

The numbers in the lines are separated by single spaces.

Output

In a single line print a real number — the answer to the problem. The answer will be considered correct, if the absolute or relative error doesn't exceed 10 - 4.

Examples

Input

3
1 2 3
3


Output

1.3333333333

Note

In the first sample the people will come in the following orders: 

  * (1, 2, 3) — there will be two people in the restaurant; 
  * (1, 3, 2) — there will be one person in the restaurant; 
  * (2, 1, 3) — there will be two people in the restaurant; 
  * (2, 3, 1) — there will be one person in the restaurant; 
  * (3, 1, 2) — there will be one person in the restaurant; 
  * (3, 2, 1) — there will be one person in the restaurant. 



In total we get (2 + 1 + 2 + 1 + 1 + 1) / 6 = 8 / 6 = 1.(3).

## Categories

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
1 2 3
3
```

**Output**:
```
1.3333333333
```

### Example 2

**Input**:
```
23
2 1 2 1 1 1 2 2 2 1 1 2 2 1 1 1 2 1 2 2 1 1 1
37
```

**Output**:
```
23.0000000000
```

### Example 3

**Input**:
```
50
1 5 2 4 3 4 1 4 1 2 5 1 4 5 4 2 1 2 5 3 4 5 5 2 1 2 2 2 2 2 3 2 5 1 2 2 3 2 5 5 1 3 4 5 2 1 3 4 2 2
29
```

**Output**:
```
9.8873093486
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
