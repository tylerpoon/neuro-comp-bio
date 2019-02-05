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
    parser.add_argument('-n', dest="N", type=int, required=True)
    parser.add_argument('-k', dest="K", type=int, required=True)    
    parser.add_argument('--steps', '-s', dest="steps", type=int, required=True)
    parser.add_argument('-d', dest="D", type=int, default=1)
    parser.add_argument('--print-every', '-p', dest='print_every', type=int, default=1)
    args = parser.parse_args()
    N = args.N
    K = args.K
    if N < K:
        parser.error("N must be greater than K")
    D = args.D
    if D < 1:
        parser.error("D must be 1 or greater")
    steps = args.steps
    print_every = args.print_every

    nodes = []
    start_state = []
    for i in range(0, N):
        bit = bool(random.getrandbits(1))
        start_state.append(bit)
        nodes.append((bit, random.sample([x for x in range(N) if x != i], K), {}))

    step_loop(nodes, steps, print_every)
    if D > 1:
        for i in range(D-1):
            print('\n\n')
            new_start_state = start_state
            flip = random.randint(0, len(nodes)-1)
            new_start_state[flip] = not new_start_state[flip]
            new_nodes = []
            for j in range(0, N):
                new_nodes.append((new_start_state[j], nodes[j][1], nodes[j][2]))
            step_loop(new_nodes, steps, print_every)

if __name__ == "__main__":
    main()
