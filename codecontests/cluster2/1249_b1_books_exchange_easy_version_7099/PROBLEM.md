# 1249_B1. Books Exchange (easy version)

**ID:** 1249_b1_books_exchange_easy_version_7099
**Difficulty:** 8

## Description

The only difference between easy and hard versions is constraints.

There are n kids, each of them is reading a unique book. At the end of any day, the i-th kid will give his book to the p_i-th kid (in case of i = p_i the kid will give his book to himself). It is guaranteed that all values of p_i are distinct integers from 1 to n (i.e. p is a permutation). The sequence p doesn't change from day to day, it is fixed.

For example, if n=6 and p=[4, 6, 1, 3, 5, 2] then at the end of the first day the book of the 1-st kid will belong to the 4-th kid, the 2-nd kid will belong to the 6-th kid and so on. At the end of the second day the book of the 1-st kid will belong to the 3-th kid, the 2-nd kid will belong to the 2-th kid and so on.

Your task is to determine the number of the day the book of the i-th child is returned back to him for the first time for every i from 1 to n.

Consider the following example: p = [5, 1, 2, 4, 3]. The book of the 1-st kid will be passed to the following kids:

  * after the 1-st day it will belong to the 5-th kid, 
  * after the 2-nd day it will belong to the 3-rd kid, 
  * after the 3-rd day it will belong to the 2-nd kid, 
  * after the 4-th day it will belong to the 1-st kid. 



So after the fourth day, the book of the first kid will return to its owner. The book of the fourth kid will return to him for the first time after exactly one day.

You have to answer q independent queries.

Input

The first line of the input contains one integer q (1 ≤ q ≤ 200) — the number of queries. Then q queries follow.

The first line of the query contains one integer n (1 ≤ n ≤ 200) — the number of kids in the query. The second line of the query contains n integers p_1, p_2, ..., p_n (1 ≤ p_i ≤ n, all p_i are distinct, i.e. p is a permutation), where p_i is the kid which will get the book of the i-th kid.

Output

For each query, print the answer on it: n integers a_1, a_2, ..., a_n, where a_i is the number of the day the book of the i-th child is returned back to him for the first time in this query.

Example

Input


6
5
1 2 3 4 5
3
2 3 1
6
4 6 2 1 5 3
1
1
4
3 4 1 2
5
5 1 2 4 3


Output


1 1 1 1 1 
3 3 3 
2 3 3 2 1 3 
1 
2 2 2 2 
4 4 4 1 4 

## Categories

- dsu
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
6
5
1 2 3 4 5
3
2 3 1
6
4 6 2 1 5 3
1
1
4
3 4 1 2
5
5 1 2 4 3
```

**Output**:
```
1 1 1 1 1
3 3 3
2 3 3 2 1 3
1
2 2 2 2
4 4 4 1 4
```

### Example 2

**Input**:
```
20
6
4 5 6 3 2 1
7
1 4 3 6 5 2 7
10
4 6 8 2 5 7 3 1 9 10
6
4 5 2 3 1 6
2
1 2
7
4 2 3 7 1 6 5
10
3 6 2 8 4 1 7 9 10 5
3
1 3 2
4
4 3 1 2
2
2 1
1
1
1
1
5
1 5 2 3 4
9
5 2 8 7 1 6 3 9 4
6
2 5 4 6 3 1
3
1 2 3
7
7 5 2 1 3 4 6
1
1
3
2 3 1
7
3 4 5 2 6 7 1
```

**Output**:
```
4 2 4 4 2 4
1 3 1 3 1 3 1
7 7 7 7 1 7 7 7 1 1
5 5 5 5 5 1
1 1
4 1 1 4 4 1 4
4 4 4 5 5 4 1 5 5 5
1 2 2
4 4 4 4
2 2
1
1
1 4 4 4 4
2 1 5 5 2 1 5 5 5
6 6 6 6 6 6
1 1 1
4 3 3 4 3 4 4
1
3 3 3
5 2 5 2 5 5 5
```

### Example 3

**Input**:
```
20
5
3 4 5 1 2
6
3 6 4 5 1 2
4
4 2 1 3
5
2 5 4 3 1
6
5 3 1 6 2 4
2
1 2
4
4 2 1 3
9
1 8 2 4 6 9 5 3 7
8
8 5 6 4 3 1 7 2
4
3 1 4 2
2
1 2
4
1 2 3 4
2
2 1
3
1 3 2
8
5 6 3 8 4 1 7 2
5
2 4 1 5 3
5
5 2 1 4 3
7
6 2 5 1 4 7 3
7
2 4 6 5 1 7 3
7
3 6 2 4 1 7 5
```

**Output**:
```
5 5 5 5 5
4 2 4 4 4 2
3 1 3 3
3 3 2 2 3
4 4 4 2 4 2
1 1
3 1 3 3
1 3 3 1 4 4 4 3 4
6 6 6 1 6 6 1 6
4 4 4 4
1 1
1 1 1 1
2 2
1 2 2
6 6 1 6 6 6 1 6
5 5 5 5 5
3 1 3 1 3
6 1 6 6 6 6 6
4 4 3 4 4 3 3
6 6 6 1 6 6 6
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
