# 44_H. Phone Number

**ID:** 44_h_phone_number_12435
**Difficulty:** 14

## Description

Alas, finding one's true love is not easy. Masha has been unsuccessful in that yet. Her friend Dasha told Masha about a way to determine the phone number of one's Prince Charming through arithmancy. 

The phone number is divined like that. First one needs to write down one's own phone numbers. For example, let's suppose that Masha's phone number is 12345. After that one should write her favorite digit from 0 to 9 under the first digit of her number. That will be the first digit of the needed number. For example, Masha's favorite digit is 9. The second digit is determined as a half sum of the second digit of Masha's number and the already written down first digit from her beloved one's number. In this case the arithmetic average equals to (2 + 9) / 2 = 5.5. Masha can round the number up or down, depending on her wishes. For example, she chooses the digit 5. Having written down the resulting digit under the second digit of her number, Masha moves to finding the third digit in the same way, i.e. finding the half sum the the third digit of her number and the second digit of the new number. The result is (5 + 3) / 2 = 4. In this case the answer is unique. Thus, every i-th digit is determined as an arithmetic average of the i-th digit of Masha's number and the i - 1-th digit of her true love's number. If needed, the digit can be rounded up or down. For example, Masha can get: 

12345 95444 Unfortunately, when Masha tried dialing the number, she got disappointed: as it turned out, the number was unavailable or outside the coverage area. But Masha won't give up. Perhaps, she rounded to a wrong digit or chose the first digit badly. That's why she keeps finding more and more new numbers and calling them. Count the number of numbers Masha calls. Masha calls all the possible numbers that can be found by the described means of arithmancy, except for, perhaps, her own one.

Input

The first line contains nonempty sequence consisting of digits from 0 to 9 — Masha's phone number. The sequence length does not exceed 50.

Output

Output the single number — the number of phone numbers Masha will dial.

Examples

Input

12345


Output

48


Input

09


Output

15

## Categories

- dp

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
09
```

**Output**:
```
15
```

### Example 2

**Input**:
```
12345
```

**Output**:
```
48
```

### Example 3

**Input**:
```
3
```

**Output**:
```
9
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
