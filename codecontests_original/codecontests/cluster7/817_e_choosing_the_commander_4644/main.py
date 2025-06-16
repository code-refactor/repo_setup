#!/usr/bin/env python3

import sys
from collections import defaultdict

class Node:
	def __init__(self, val):
		self.val = val
		self.left = None
		self.right = None

q = int(sys.stdin.readline())
root = Node(0)
# def search(node, bit, )

for _ in range(q):
	l = list(map(int, sys.stdin.readline().split()))
	if l[0] == 1:
		# add
		bit = 28
		cur = root
		num = l[1]
		# print(num,'num')
		while bit >= 0:
			if ((1<<bit)&num) == (1<<bit):
				if cur.right is None:
					cur.right = Node(1)
					# print(bit,'bit right')
				else:
					cur.right.val += 1
					# print(bit,'bit add right')
				cur = cur.right
			else:
				if cur.left is None:
					cur.left = Node(1)
					# print(bit,'bit  left', cur.left.val)
				else:
					cur.left.val += 1
					# print(bit,'bit add left', cur.left.val)
				cur = cur.left
			bit -= 1
	if l[0] == 2:
		num = l[1]
		bit, cur = 28, root
		# print(num,'num')
		while bit >= 0:
			if((1<<bit)&num) == (1<<bit):
				cur.right.val -= 1
				cur = cur.right
			else:
				cur.left.val -= 1
				cur = cur.left
			bit -= 1
		# remove
	if l[0] == 3:
		# print
		res, cur, bit = 0, root, 28
		# print(res, cur, bit)
		while bit >= 0:
			num = (1<<bit)
			# print(bit,'bit')
			if (num&l[2]) and (num&l[1]):
				# print("A")
				if cur.right is not None:
					res += cur.right.val
				if cur.left is None:
					break
				cur = cur.left
				bit -= 1
				continue
			if (num&l[2]) and not (num&l[1]):
				# print("B")
				if cur.left is not None:
					res += cur.left.val
				if cur.right is None:
					break
				cur = cur.right
				bit -= 1
				continue
			if not (num&l[2]) and (num&l[1]):
				# print("C")
				if cur.right is None:
					break
				cur = cur.right
				bit -= 1
				continue
			if not (num&l[2]) and not (num&l[1]):
				# print("D")
				if cur.left is None:
					break
				cur = cur.left
				bit -= 1
				continue
		print(res)

