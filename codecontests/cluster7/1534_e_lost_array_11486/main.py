from library import read_ints
from sys import stdout

def reverse(n, req):return [x for x in range(1, n + 1) if x not in req]
def solve():
    n, k = read_ints()
    if n % 2 == 1 and k % 2 == 0:print(-1);stdout.flush();return
    elif n % k == 0:
        xor = 0;curr_idx = 1
        while curr_idx <= n:next_idx = curr_idx + k;print('?', ' '.join(str(x) for x in range(curr_idx, next_idx)));stdout.flush();xor ^= int(input());curr_idx = next_idx
        print('!', xor);stdout.flush();return
    elif n%2 != k%2 and n < 2 * k:
        xor = 0;curr_idx = 1;kk = n - k
        while True:
            next_idx = curr_idx + kk;curr_arr = reverse(n, set(range(curr_idx, next_idx)));print('?', ' '.join(str(x) for x in curr_arr));stdout.flush();xor ^= int(input());curr_idx = next_idx
            if (n - curr_idx + 1) < 2 * kk and (n - curr_idx + 1) % 2 == 0:break
        if curr_idx < n:
            arr = list(range(1, kk+1));next_idx = curr_idx + (n - curr_idx + 1) // 2;curr_arr = list(range(curr_idx, next_idx)) + arr
            curr_arr = reverse(n, set(curr_arr[:kk]));print('?', ' '.join(str(x) for x in curr_arr));stdout.flush();xor ^= int(input())
            curr_arr = list(range(next_idx, n+1)) + arr;curr_arr = reverse(n, set(curr_arr[:kk]));print('?', ' '.join(str(x) for x in curr_arr));stdout.flush();xor ^= int(input())
        print('!', xor);stdout.flush();return
    else:
        xor = 0
        curr_idx = 1
        while True:
            next_idx = curr_idx + k
            print('?', ' '.join(str(x) for x in range(curr_idx, next_idx)))
            stdout.flush()
            xor ^= int(input())
            curr_idx = next_idx
            if (n - curr_idx + 1) < 2 * k and (n - curr_idx + 1) % 2 == 0:
                break
        if curr_idx < n:
            arr = list(range(1, k+1))
            next_idx = curr_idx + (n - curr_idx + 1) // 2

            curr_arr = list(range(curr_idx, next_idx)) + arr
            print('?', ' '.join(str(x) for x in curr_arr[:k]))
            stdout.flush()
            xor ^= int(input())

            curr_arr = list(range(next_idx, n+1)) + arr
            print('?', ' '.join(str(x) for x in curr_arr[:k]))
            stdout.flush()
            xor ^= int(input())
        print('!', xor)
        stdout.flush()
        return
if __name__ == '__main__':solve()