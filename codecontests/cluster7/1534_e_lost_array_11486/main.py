#!/usr/bin/env python3

from sys import stdout
from library import read_ints

def reverse(n, req):
    """Return numbers from 1 to n that are not in req."""
    return [x for x in range(1, n + 1) if x not in req]

def solve():
    n, k = read_ints()
    
    # Case 1: Impossible case - odd n and even k
    if n % 2 == 1 and k % 2 == 0:
        print(-1)
        stdout.flush()
        return
    
    # Case 2: n is divisible by k - simplest case
    elif n % k == 0:
        xor = 0
        curr_idx = 1
        while curr_idx <= n:
            next_idx = curr_idx + k
            # Query k consecutive elements
            print('?', ' '.join(str(x) for x in range(curr_idx, next_idx)))
            stdout.flush()
            xor ^= int(input())
            curr_idx = next_idx
        
        print('!', xor)
        stdout.flush()
        return
    
    # Case 3: n and k have different parity and n < 2*k
    elif n % 2 != k % 2 and n < 2 * k:
        xor = 0
        curr_idx = 1
        kk = n - k  # Use complement size
        
        while True:
            next_idx = curr_idx + kk
            # Query the complement of kk consecutive elements
            curr_arr = reverse(n, set(range(curr_idx, next_idx)))
            print('?', ' '.join(str(x) for x in curr_arr))
            stdout.flush()
            xor ^= int(input())
            curr_idx = next_idx
            
            # Break when remaining elements are not enough and have even parity
            if (n - curr_idx + 1) < 2 * kk and (n - curr_idx + 1) % 2 == 0:
                break
        
        # Handle remaining elements if any
        if curr_idx <= n:
            arr = list(range(1, kk + 1))
            next_idx = curr_idx + (n - curr_idx + 1) // 2
            
            # First query for remaining elements
            curr_arr = list(range(curr_idx, next_idx)) + arr
            curr_arr = reverse(n, set(curr_arr[:kk]))
            print('?', ' '.join(str(x) for x in curr_arr))
            stdout.flush()
            xor ^= int(input())
            
            # Second query for remaining elements
            curr_arr = list(range(next_idx, n + 1)) + arr
            curr_arr = reverse(n, set(curr_arr[:kk]))
            print('?', ' '.join(str(x) for x in curr_arr))
            stdout.flush()
            xor ^= int(input())
        
        print('!', xor)
        stdout.flush()
        return
    
    # Case 4: General case
    else:
        xor = 0
        curr_idx = 1
        
        while True:
            next_idx = curr_idx + k
            # Query k consecutive elements
            print('?', ' '.join(str(x) for x in range(curr_idx, next_idx)))
            stdout.flush()
            xor ^= int(input())
            curr_idx = next_idx
            
            # Break when remaining elements are not enough and have even parity
            if (n - curr_idx + 1) < 2 * k and (n - curr_idx + 1) % 2 == 0:
                break
        
        # Handle remaining elements if any
        if curr_idx <= n:
            arr = list(range(1, k + 1))
            next_idx = curr_idx + (n - curr_idx + 1) // 2
            
            # First query for remaining elements
            curr_arr = list(range(curr_idx, next_idx)) + arr
            print('?', ' '.join(str(x) for x in curr_arr[:k]))
            stdout.flush()
            xor ^= int(input())
            
            # Second query for remaining elements
            curr_arr = list(range(next_idx, n + 1)) + arr
            print('?', ' '.join(str(x) for x in curr_arr[:k]))
            stdout.flush()
            xor ^= int(input())
        
        print('!', xor)
        stdout.flush()
        return

if __name__ == '__main__':
    solve()