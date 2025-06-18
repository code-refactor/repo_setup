"""
Library file for cluster7.
This contains shared code that can be imported by problems in this cluster.
"""
import sys
from collections import defaultdict, Counter

def read_int():
    """Read a single integer from input."""
    return int(input())

def read_ints():
    """Read multiple integers from a single line."""
    return map(int, input().split())

def read_array():
    """Read an array of integers from a single line."""
    return list(map(int, input().split()))

def yes_no(condition, yes_str="YES", no_str="NO"):
    """Print YES/NO based on condition."""
    print(yes_str if condition else no_str)

def xor_array(arr):
    """XOR of all elements in array."""
    result = 0
    for x in arr:
        result ^= x
    return result

def xor_prefix(arr):
    """Generate XOR prefix array, starting with 0."""
    result = [0]
    for x in arr:
        result.append(result[-1] ^ x)
    return result

def xor_range(arr, start, end):
    """XOR of elements in range [start, end) using prefix array."""
    prefix = xor_prefix(arr)
    return prefix[end] ^ prefix[start]

def find_k(arr):
    """
    Find smallest k where applying XOR k to all elements preserves the set.
    Returns -1 if no such k exists.
    """
    n = len(arr)
    arr_set = set(arr)
    max_val = max(arr)
    
    for k in range(1, 2*max_val + 1):
        valid = True
        for num in arr:
            if (num ^ k) not in arr_set:
                valid = False
                break
        if valid:
            return k
    return -1

def count_frequency(arr):
    """Count frequency of each element in array."""
    freq = {}
    for x in arr:
        freq[x] = freq.get(x, 0) + 1
    return freq

def is_all_equal(arr):
    """Check if all elements in array are equal."""
    return len(set(arr)) <= 1

def xor_transform(arr, k):
    """Apply XOR with k to all elements in array."""
    return [x ^ k for x in arr]

def min_max(arr):
    """Return minimum and maximum of array."""
    return min(arr), max(arr)

class BitTrieNode:
    """A trie node for bit operations."""
    def __init__(self, val=0):
        self.val = val  # Count of numbers ending at this node
        self.left = None  # 0 bit
        self.right = None  # 1 bit
        
class XorTrieNode:
    """A simplified trie node for XOR operations."""
    def __init__(self):
        self.children = [0, 0]  # [left (0), right (1)]
        self.count = 0          # Count of elements in subtree

class BitTrie:
    """A trie for bit operations, useful for XOR-based queries."""
    def __init__(self, bit_length=30):
        self.root = BitTrieNode(0)
        self.bit_length = bit_length
        
# Common prime numbers up to 70
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]

def get_prime_signature(num, primes=PRIMES):
    """Convert a number to its prime signature (binary representation of prime factors)."""
    signature = 0
    for i, p in enumerate(primes):
        count = 0
        while num % p == 0:
            num //= p
            count += 1
        # If count is odd, set the corresponding bit
        if count % 2 == 1:
            signature |= (1 << i)
    return signature

def mod_pow(base, exp, mod):
    """Calculate (base ^ exp) % mod efficiently."""
    return pow(base, exp, mod)

def solve_triple_flips(a):
    """Solve the triple flips problem. Find sequence of triple flips to convert array to all zeros."""
    l = len(a)
    d = sum(a[i] * 2 ** i for i in range(l))
    
    # If array is already all zeros, no flips needed
    if d == 0:
        return []
    
    # Generate possible flip patterns
    usable = []
    # 3 consecutive 1s: 0b111
    if l >= 3:
        for i in range(l - 2):
            usable.append(0b111 << i)
    # 5-bit pattern with alternating 1s: 0b10101
    if l >= 5:
        for i in range(l - 4):
            usable.append(0b10101 << i)
    # 7-bit pattern with 1s at positions 0,3,6: 0b1001001
    if l >= 7:
        for i in range(l - 6):
            usable.append(0b1001001 << i)
    
    # Try all combinations of flip patterns
    ul = len(usable)
    best_answer = None
    
    # Iterate through all possible combinations of flip patterns
    for mask in range(1 << ul):
        start = 0
        clone = mask
        cnt = 0
        # Calculate XOR of all selected patterns
        while clone:
            if clone % 2 == 1:
                start ^= usable[cnt]
            clone //= 2
            cnt += 1
        
        # If this combination of flips converts the array to all zeros
        if start == d:
            answer = []
            clone = mask
            cnt = 0
            # Create the list of flips
            while clone:
                if clone % 2 == 1:
                    answer.append([])
                    used = usable[cnt]
                    cnt2 = 1
                    # Convert bit pattern to indices
                    while used:
                        if used % 2 == 1:
                            answer[-1].append(cnt2)
                        cnt2 += 1
                        used //= 2
                clone //= 2
                cnt += 1
            
            # Keep the shortest answer
            if best_answer is None or len(best_answer) > len(answer):
                best_answer = answer
    
    return best_answer

def solve_triple_flips_large(a):
    """Solve the triple flips problem for large arrays."""
    operations = []
    # Reduce array to size 10 or less
    while len(a) > 10:
        l = len(a)
        last = a[-3:]
        
        if last == [1, 1, 1]:
            operations.append([l - 2, l - 1, l])
        elif last == [1, 1, 0]:
            operations.append([l - 3, l - 2, l - 1])
            a[-4] ^= 1
        elif last == [1, 0, 1]:
            operations.append([l - 4, l - 2, l])
            a[-5] ^= 1
        elif last == [0, 1, 1]:
            nxt = a[-6:-3]
            if nxt == [1, 1, 1]:
                operations.append([l - 8, l - 4, l])
                operations.append([l - 5, l - 3, l - 1])
                a[-9] ^= 1
            elif nxt == [1, 1, 0]:
                operations.append([l - 8, l - 4, l])
                operations.append([l - 9, l - 5, l - 1])
                a[-9] ^= 1
                a[-10] ^= 1
            elif nxt == [1, 0, 1]:
                operations.append([l - 6, l - 3, l])
                operations.append([l - 9, l - 5, l - 1])
                a[-7] ^= 1
                a[-10] ^= 1
            elif nxt == [0, 1, 1]:
                operations.append([l - 6, l - 3, l])
                operations.append([l - 7, l - 4, l - 1])
                a[-7] ^= 1
                a[-8] ^= 1
            elif nxt == [1, 0, 0]:
                operations.append([l - 2, l - 1, l])
                operations.append([l - 8, l - 5, l - 2])
                a[-9] ^= 1
            elif nxt == [0, 1, 0]:
                operations.append([l - 2, l - 1, l])
                operations.append([l - 6, l - 4, l - 2])
                a[-7] ^= 1
            elif nxt == [0, 0, 1]:
                operations.append([l - 10, l - 5, l])
                operations.append([l - 5, l - 3, l - 1])
                a[-11] ^= 1
            elif nxt == [0, 0, 0]:
                operations.append([l - 8, l - 4, l])
                operations.append([l - 7, l - 4, l - 1])
                a[-9] ^= 1
                a[-8] ^= 1
            a.pop()
            a.pop()
            a.pop()
        elif last == [1, 0, 0]:
            operations.append([l - 4, l - 3, l - 2])
            a[-5] ^= 1
            a[-4] ^= 1
        elif last == [0, 1, 0]:
            operations.append([l - 5, l - 3, l - 1])
            a[-6] ^= 1
            a[-4] ^= 1
        elif last == [0, 0, 1]:
            operations.append([l - 6, l - 3, l])
            a[-7] ^= 1
            a[-4] ^= 1
        a.pop()
        a.pop()
        a.pop()
    
    # Pad array to ensure it's at least 8 elements long
    while len(a) < 8:
        a.append(0)
    
    # Solve the small array
    sol = solve_triple_flips(a)
    
    # Combine results
    return operations + sol if sol else None
    
    def insert(self, num):
        """Insert a number into the trie."""
        cur = self.root
        for bit in range(self.bit_length, -1, -1):
            if (1 << bit) & num:
                if cur.right is None:
                    cur.right = BitTrieNode(1)
                else:
                    cur.right.val += 1
                cur = cur.right
            else:
                if cur.left is None:
                    cur.left = BitTrieNode(1)
                else:
                    cur.left.val += 1
                cur = cur.left
    
    def remove(self, num):
        """Remove a number from the trie."""
        cur = self.root
        for bit in range(self.bit_length, -1, -1):
            if (1 << bit) & num:
                cur.right.val -= 1
                cur = cur.right
            else:
                cur.left.val -= 1
                cur = cur.left
    
    def count_xor_queries(self, p, l):
        """Count elements with XOR query (p XOR element) >= l."""
        res, cur = 0, self.root
        bit = self.bit_length
        
        while bit >= 0 and cur is not None:
            mask = (1 << bit)
            p_bit = bool(mask & p)
            l_bit = bool(mask & l)
            
            if l_bit and p_bit:  # Both bits are 1
                if cur.right is not None:
                    res += cur.right.val
                cur = cur.left
            elif l_bit and not p_bit:  # L bit is 1, P bit is 0
                if cur.left is not None:
                    res += cur.left.val
                cur = cur.right
            elif not l_bit and p_bit:  # L bit is 0, P bit is 1
                cur = cur.right
            else:  # Both bits are 0
                cur = cur.left
            
            bit -= 1
        
        return res
    
class XorTrie:
    """A trie optimized for XOR operations."""
    def __init__(self, bit_length=30):
        self.tree = [[0, 0, 0]]  # [left_child, right_child, count]
        self.bit_length = bit_length
    
    def add(self, x):
        """Add a number to the trie."""
        now = 0
        self.tree[now][2] += 1  # Increment root count
        
        for i in range(self.bit_length, -1, -1):
            bit = (x >> i) & 1
            if self.tree[now][bit] == 0:
                self.tree[now][bit] = len(self.tree)
                self.tree.append([0, 0, 0])
            now = self.tree[now][bit]
            self.tree[now][2] += 1
    
    def find_min_xor(self, x):
        """Find the value in the trie that produces minimum XOR with x and remove it."""
        now = ans = 0
        
        for i in range(self.bit_length, -1, -1):
            bit = (x >> i) & 1
            if self.tree[now][bit] and self.tree[self.tree[now][bit]][2]:
                now = self.tree[now][bit]
            else:
                now = self.tree[now][bit ^ 1]
                ans |= (1 << i)
            self.tree[now][2] -= 1
            
        return ans