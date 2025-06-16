from library import read_array, CountingXORTrie

n = int(input())
a = read_array(n)
b = read_array(n)

trie = CountingXORTrie(30)
for x in b:
    trie.insert(x)

for x in a:
    print(trie.query_min_xor_remove(x), end=' ')