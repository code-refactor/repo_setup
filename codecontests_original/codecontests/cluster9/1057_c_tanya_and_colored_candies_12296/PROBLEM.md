# 1057_C. Tanya and Colored Candies

**ID:** 1057_c_tanya_and_colored_candies_12296
**Difficulty:** 9

## Description

There are n candy boxes in front of Tania. The boxes are arranged in a row from left to right, numbered from 1 to n. The i-th box contains r_i candies, candies have the color c_i (the color can take one of three values ​​— red, green, or blue). All candies inside a single box have the same color (and it is equal to c_i).

Initially, Tanya is next to the box number s. Tanya can move to the neighbor box (that is, with a number that differs by one) or eat candies in the current box. Tanya eats candies instantly, but the movement takes one second.

If Tanya eats candies from the box, then the box itself remains in place, but there is no more candies in it. In other words, Tanya always eats all the candies from the box and candies in the boxes are not refilled.

It is known that Tanya cannot eat candies of the same color one after another (that is, the colors of candies in two consecutive boxes from which she eats candies are always different). In addition, Tanya's appetite is constantly growing, so in each next box from which she eats candies, there should be strictly more candies than in the previous one.

Note that for the first box from which Tanya will eat candies, there are no restrictions on the color and number of candies.

Tanya wants to eat at least k candies. What is the minimum number of seconds she will need? Remember that she eats candies instantly, and time is spent only on movements.

Input

The first line contains three integers n, s and k (1 ≤ n ≤ 50, 1 ≤ s ≤ n, 1 ≤ k ≤ 2000) — number of the boxes, initial position of Tanya and lower bound on number of candies to eat. The following line contains n integers r_i (1 ≤ r_i ≤ 50) — numbers of candies in the boxes. The third line contains sequence of n letters 'R', 'G' and 'B', meaning the colors of candies in the correspondent boxes ('R' for red, 'G' for green, 'B' for blue). Recall that each box contains candies of only one color. The third line contains no spaces.

Output

Print minimal number of seconds to eat at least k candies. If solution doesn't exist, print "-1".

Examples

Input

5 3 10
1 2 3 4 5
RGBRR


Output

4


Input

2 1 15
5 6
RG


Output

-1

Note

The sequence of actions of Tanya for the first example:

  * move from the box 3 to the box 2; 
  * eat candies from the box 2; 
  * move from the box 2 to the box 3; 
  * eat candy from the box 3; 
  * move from the box 3 to the box 4; 
  * move from the box 4 to the box 5; 
  * eat candies from the box 5. 



Since Tanya eats candy instantly, the required time is four seconds.

## Categories

- *special
- dp

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2 1 15
5 6
RG
```

**Output**:
```
-1
```

### Example 2

**Input**:
```
5 3 10
1 2 3 4 5
RGBRR
```

**Output**:
```
4
```

### Example 3

**Input**:
```
30 28 208
3 42 42 47 46 44 5 28 35 28 35 44 25 44 47 3 3 35 28 5 3 42 3 46 25 25 5 47 46 3
BGBBGBBBBGRRGGGBRGRGRRGBBRRRRG
```

**Output**:
```
20
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
