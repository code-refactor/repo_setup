#!/usr/bin/env python3

# _
#####################################################################################################################

def minCo_growingSequenceWith(array):
    sequence, prevValue = [], 0
    for value in array:
        n = prevValue&(prevValue^value)
        prevValue = value^n
        sequence.append(n)

    return ' '.join(map(str, sequence))


def testCase_1547d():
    input()
    return map(int, input().split(' '))


tuple(print(minCo_growingSequenceWith(testCase_1547d())) for x in range(int(input())))
