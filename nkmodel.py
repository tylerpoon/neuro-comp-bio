import random
import sys
import argparse

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

def step_loop(nodes, steps, print_every=1):
    print('start: ', end='')
    print_nodes(nodes)
    for i in range(steps):
        nodes = step(nodes)
        if i % print_every == 0:
            print(str(i + 1) + ': ', end='')
            print_nodes(nodes)

def main():
    parser = argparse.ArgumentParser(description='NK Model Parameter handler')
    parser.add_argument('-N', dest="N", type=int, required=True)
    parser.add_argument('-K', dest="K", type=int, required=True)    
    parser.add_argument('--steps', '-s', dest="steps", type=int, required=True)
    parser.add_argument('--print-every', '-p', dest='print_every', type=int, default=1)
    args = parser.parse_args()
    N = args.N
    K = args.K
    if N < K:
        parser.error("N must be greater than K")
    steps = args.steps
    print_every = args.print_every

    nodes = []
    for i in range(0, N):
        nodes.append((bool(random.getrandbits(1)), random.sample([x for x in range(N) if x != i], K), {}))

    step_loop(nodes, steps, print_every)

main()