# 50_D. Bombing

**ID:** 50_d_bombing_7752
**Difficulty:** 10

## Description

The commanding officers decided to drop a nuclear bomb on the enemy's forces. You are ordered to determine the power of the warhead that needs to be used.

The enemy has N strategically important objects. Their positions are known due to the intelligence service. The aim of the strike is to deactivate at least K important objects of the enemy. The bombing impact point is already determined and has coordinates of [X0; Y0].

The nuclear warhead is marked by the estimated impact radius R ≥ 0. All the buildings that are located closer than R to the bombing epicentre will be destroyed. All the buildings that are located further than R from the epicentre, can also be deactivated with some degree of probability. Let's assume that D is the distance between a building and the epicentre. This building's deactivation probability P(D, R) is calculated according to the following formula: 

<image> We should regard <image> as ea, where e ≈ 2.7182818284590452353602874713527

If the estimated impact radius of the warhead is equal to zero, then all the buildings located in the impact point will be completely demolished and all the rest of important objects will not be damaged.

The commanding officers want the probability of failing the task to be no more than ε. Nuclear warheads are too expensive a luxury, that's why you have to minimise the estimated impact radius of the warhead. 

Input

The first line contains an integer N which represents the number of the enemy's objects (1 ≤ N ≤ 100). The second line contains two integers: K is the required number of deactivated objects, and ε is the maximally permitted probability of not completing the task, given in per mils (1 ≤ K ≤ N, 1 ≤ ε ≤ 999). The third line contains X0 and Y0 which are the coordinates of the strike impact point. The next N lines contain two numbers Xi and Yi each which are the coordinates of every strategically important object. All the coordinates are integer, their absolute values do not exceed 1000.

Let us remind you that there are a thousand per mils in unity (number one).

There can be several objects in one point.

Output

Print the sought estimated impact radius of the warhead. The absolute or relative measure of the inaccuracy of your answer should not exceed 10 - 6.

Examples

Input

1
1 500
5 5
1 2


Output

3.84257761518762740


Input

5
3 100
0 0
3 4
60 70
100 100
10 10
5 12


Output

13.45126176453737600

## Categories

- binary search
- dp
- probabilities

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5
3 100
0 0
3 4
60 70
100 100
10 10
5 12
```

**Output**:
```
13.451261761474598
```

### Example 2

**Input**:
```
1
1 500
5 5
1 2
```

**Output**:
```
3.842577611976594
```

### Example 3

**Input**:
```
3
2 17
0 0
1 0
35 27
0 5
```

**Output**:
```
4.957678079335892
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
