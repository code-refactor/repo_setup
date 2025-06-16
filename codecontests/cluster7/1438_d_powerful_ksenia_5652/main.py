from library import read_array, xor_array

def main():
    n = int(input())
    l = read_array(n)
    if n % 2 == 0:
        if xor_array(l) != 0:
            print('NO')
            return
    print('YES')
    z = (n - 1) // 2
    print(2 * z)
    for i in range(z):
        print(2*i+1, 2*i+2, n)
    for i in range(z):
        print(2*i+1, 2*i+2, n)
if __name__ == '__main__':
    main()