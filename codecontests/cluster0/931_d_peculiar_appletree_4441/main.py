from library import *

n = int_inp()
tree = [{'length': 0}]

for x in input().split():
    parent = int(x)
    length = 0 if parent == 0 else tree[parent-1]['length'] + 1
    tree.append({'length': length})

# Count frequencies of lengths and sum odd values
length_counts = counter_dict([node['length'] for node in tree])
print(sum(count & 1 for count in length_counts.values()))
