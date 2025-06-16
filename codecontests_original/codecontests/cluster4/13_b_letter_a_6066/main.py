#!/usr/bin/env python3

__author__ = 'Darren'


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

        nonlocal vector1, vector2, vector3, vector4
        vector1 = Vector2D(segments[0][0], segments[0][1])
        vector2 = Vector2D(segments[1][0], segments[1][1])
        vector3 = Vector2D(segments[0][0], segments[2][0])
        vector4 = Vector2D(segments[1][0], segments[2][1])
        if vector1.parallel(vector3):
            return vector2.parallel(vector4)
        else:
            vector3 = Vector2D(segments[0][0], segments[2][1])
            vector4 = Vector2D(segments[1][0], segments[2][0])
            return vector1.parallel(vector3) and vector2.parallel(vector4)

    def check_condition_2():
        return vector1.acute_or_perpendicular(vector2)

    def check_condition_3():
        return (0.2 <= vector1.dot_product(vector3) / vector1.distance_square() <= 0.8 and
                0.2 <= vector2.dot_product(vector4) / vector2.distance_square() <= 0.8)

    segments = []
    for _i in range(3):
        temp = [int(x) for x in input().split()]
        segments.append([(temp[0], temp[1]), (temp[2], temp[3])])
    vector1, vector2, vector3, vector4 = None, None, None, None
    if check_condition_1() and check_condition_2() and check_condition_3():
        print('YES')
    else:
        print('NO')


class Vector2D:
    def __init__(self, p1, p2):
        self.x = p2[0] - p1[0]
        self.y = p2[1] - p1[1]

    def distance_square(self):
        return self.x ** 2 + self.y ** 2

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y

    def cross_product(self, other):
        return self.x * other.y - self.y * other.x

    def parallel(self, other):
        return self.cross_product(other) == 0

    def acute_or_perpendicular(self, other):
        return self.dot_product(other) >= 0 and not self.parallel(other)


if __name__ == '__main__':
    solve()