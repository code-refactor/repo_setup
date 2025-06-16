#!/usr/bin/env python3

from collections import Counter

tree = []


class Node:
    def __init__(self, num=None):
        self.length = 0 if num is None else tree[num-1].length + 1


def main():
    n = int(input())
    global tree
    tree = [Node()]

    for x in input().split():
        tree.append(Node(int(x)))

    print(sum([value & 1 for key, value in Counter([x.length for x in tree]).items()]))


if __name__ == "__main__":
    main()
