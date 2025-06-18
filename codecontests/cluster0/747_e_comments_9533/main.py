#!/usr/bin/env python3

from library import fast_input
from collections import deque

def parse_comments(s):
    # Split the input by commas
    tokens = s.split(',')
    n = len(tokens) // 2
    
    # Parse comments and their children counts
    comments = [(tokens[2*i], int(tokens[2*i+1])) for i in range(n)]

    # Data structures for building the comment tree
    stack = []
    graph = {i: [] for i in range(n+1)}  # Adjacency list representation
    comment_text = {}  # Store the text of each comment
    depth = {i: 0 for i in range(n+1)}  # Track the depth of each comment
    
    # Process comments in reverse order
    for i, (text, child_count) in enumerate(reversed(comments)):
        comment_id = i + 1
        comment_text[comment_id] = text
        
        # Get the children from the stack
        for j in range(child_count):
            child_id = stack.pop()
            graph[comment_id].append(child_id)
            # Update depth based on children
            depth[comment_id] = max(depth[comment_id], depth[child_id])

        # Increment depth for this comment
        depth[comment_id] += 1
        stack.append(comment_id)

    # Root node handling (virtual root)
    graph[0].extend(reversed(stack))
    depth[0] = max(depth[i] for i in stack) + 1 if stack else 1
    comment_text[0] = None

    # BFS to organize comments by level
    queue = deque([0])
    result = [[] for _ in range(depth[0])]
    
    while queue:
        node = queue.popleft()
        d = depth[node] - 1
        if comment_text[node] is not None:  # Skip the virtual root's text
            result[d].append(comment_text[node])
        
        for child in graph[node]:
            depth[child] = d
            queue.append(child)

    # Remove the level for the virtual root
    result.pop()
    return result

# Read input
input_str = input().rstrip()

# Parse comments
comment_levels = parse_comments(input_str)

# Print results
print(len(comment_levels))
for level in reversed(comment_levels):
    print(' '.join(level))
