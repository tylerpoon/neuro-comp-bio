import random
import sys

def step(nodes):
    new_nodes = []
    for n in nodes: 
        in_bits = sum([1<<i for i, b in enumerate(map(lambda x: nodes[x][0], n[1])) if b])
        if in_bits not in n[2]:
            n[2][in_bits] = bool(random.getrandbits(1))
        new_nodes.append((n[2][in_bits], n[1], n[2]))
        
    return new_nodes

def print_nodes(nodes):
    print(''.join(['1' if n[0] else '0' for n in nodes]))

N = int(input("N: "))
K = int(input("K: "))

if N < K:
    print('K can\'t be bigger than N!')
    sys.exit()

steps = int(input("Steps: "))

nodes = []

for i in range(0, N):
    nodes.append((bool(random.getrandbits(1)), random.sample([x for x in range(N) if x != i], K), {}))

print('start: ', end='')
print_nodes(nodes)
for i in range(steps):
    nodes = step(nodes)
    print(str(i + 1) + ': ', end='')
    print_nodes(nodes)
