# 2_C. Commentator problem

**ID:** 2_c_commentator_problem_4414
**Difficulty:** 9

## Description

The Olympic Games in Bercouver are in full swing now. Here everyone has their own objectives: sportsmen compete for medals, and sport commentators compete for more convenient positions to give a running commentary. Today the main sport events take place at three round stadiums, and the commentator's objective is to choose the best point of observation, that is to say the point from where all the three stadiums can be observed. As all the sport competitions are of the same importance, the stadiums should be observed at the same angle. If the number of points meeting the conditions is more than one, the point with the maximum angle of observation is prefered. 

Would you, please, help the famous Berland commentator G. Berniev to find the best point of observation. It should be noted, that the stadiums do not hide each other, the commentator can easily see one stadium through the other.

Input

The input data consists of three lines, each of them describes the position of one stadium. The lines have the format x, y, r, where (x, y) are the coordinates of the stadium's center ( - 103 ≤ x, y ≤ 103), and r (1 ≤ r ≤ 103) is its radius. All the numbers in the input data are integer, stadiums do not have common points, and their centers are not on the same line. 

Output

Print the coordinates of the required point with five digits after the decimal point. If there is no answer meeting the conditions, the program shouldn't print anything. The output data should be left blank.

Examples

Input

0 0 10
60 0 10
30 30 10


Output

30.00000 0.00000

## Categories

- geometry

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
0 0 10
60 0 10
30 30 10
```

**Output**:
```
30.00000 0.00000
```

### Example 2

**Input**:
```
0 0 10
300 300 13
500 -500 16
```

**Output**:
```
282.61217 -82.24022
```

### Example 3

**Input**:
```
0 0 10
300 300 12
500 -500 14
```

**Output**:
```
311.34912 -88.13335
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
