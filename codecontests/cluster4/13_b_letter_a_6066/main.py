#!/usr/bin/env python3

from library import Vector2D


def solve():
    t = int(input())
    while t:
        run()
        t -= 1


def run():
    def check_condition_1():
        record = {}
        common, first, second = None, -1, -1
        found = False
        for i in range(3):
            for j in range(2):
                if segments[i][j] in record:
                    if found:
                        return False
                    found = True
                    common = segments[i][j]
                    first, second = record[segments[i][j]], i
                else:
                    record[segments[i][j]] = i
        if not found:
            return False

        segments[0], segments[first] = segments[first], segments[0]
        segments[1], segments[second] = segments[second], segments[1]
        if common != segments[0][0]:
            segments[0][0], segments[0][1] = segments[0][1], segments[0][0]
        if common != segments[1][0]:
            segments[1][0], segments[1][1] = segments[1][1], segments[1][0]

        def make_vector(p1, p2):
            return Vector2D(p2[0] - p1[0], p2[1] - p1[1])
        
        def parallel(v1, v2):
            return v1.cross(v2) == 0
        
        nonlocal vector1, vector2, vector3, vector4
        vector1 = make_vector(segments[0][0], segments[0][1])
        vector2 = make_vector(segments[1][0], segments[1][1])
        vector3 = make_vector(segments[0][0], segments[2][0])
        vector4 = make_vector(segments[1][0], segments[2][1])
        if parallel(vector1, vector3):
            return parallel(vector2, vector4)
        else:
            vector3 = make_vector(segments[0][0], segments[2][1])
            vector4 = make_vector(segments[1][0], segments[2][0])
            return parallel(vector1, vector3) and parallel(vector2, vector4)

    def check_condition_2():
        return vector1.dot(vector2) >= 0 and vector1.cross(vector2) != 0

    def check_condition_3():
        return (0.2 <= vector1.dot(vector3) / vector1.norm_squared() <= 0.8 and
                0.2 <= vector2.dot(vector4) / vector2.norm_squared() <= 0.8)

    segments = []
    for _i in range(3):
        temp = [int(x) for x in input().split()]
        segments.append([(temp[0], temp[1]), (temp[2], temp[3])])
    vector1, vector2, vector3, vector4 = None, None, None, None
    if check_condition_1() and check_condition_2() and check_condition_3():
        print('YES')
    else:
        print('NO')




if __name__ == '__main__':
    solve()