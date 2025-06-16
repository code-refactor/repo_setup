from library import read_array

def minCo_growingSequenceWith(array):
    sequence, prevValue = [], 0
    for value in array:
        n = prevValue & (prevValue ^ value)
        prevValue = value ^ n
        sequence.append(n)
    return ' '.join(map(str, sequence))

for _ in range(int(input())):
    n = int(input())
    array = read_array(n)
    print(minCo_growingSequenceWith(array))
