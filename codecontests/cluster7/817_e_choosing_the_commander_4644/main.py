from library import read_ints, get_bit
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
	l = read_ints()
	if l[0] == 1:
		# add
		bit = 28
		cur = root
		num = l[1]
		# print(num,'num')
		while bit >= 0:
			if get_bit(num, bit):
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
			if get_bit(num, bit):
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
			if get_bit(l[2], bit) and get_bit(l[1], bit):
				# print("A")
				if cur.right is not None:
					res += cur.right.val
				if cur.left is None:
					break
				cur = cur.left
				bit -= 1
				continue
			if get_bit(l[2], bit) and not get_bit(l[1], bit):
				# print("B")
				if cur.left is not None:
					res += cur.left.val
				if cur.right is None:
					break
				cur = cur.right
				bit -= 1
				continue
			if not get_bit(l[2], bit) and get_bit(l[1], bit):
				# print("C")
				if cur.right is None:
					break
				cur = cur.right
				bit -= 1
				continue
			if not get_bit(l[2], bit) and not get_bit(l[1], bit):
				# print("D")
				if cur.left is None:
					break
				cur = cur.left
				bit -= 1
				continue
		print(res)

