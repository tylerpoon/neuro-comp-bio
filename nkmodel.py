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

def print_state(state):
    print(''.join(['1' if s else '0' for s in state]))

def print_attractor(s):
    sset = set()
    attract_start = []
    attract_end_index = 0
    num_s = []
    for v in s:
        num_s.append(sum([1<<i for i, b in enumerate(v) if b]))

    for i, v in enumerate(num_s):
        if v in sset:
            attract_start = v
            attract_end_index = i
            break;
        else:
            sset.add(v)

    if attract_start == []:
        return;

    attract_start_index = num_s.index(attract_start)

    attractor = s[attract_start_index:attract_end_index]
    print("\nAttractor:")
    for i, s in enumerate(attractor):
        print_state(s)
        print('↓')
    print_state(attractor[0])

def step_loop(nodes, steps, print_every=1):
    states = [[]]
    print('start: ', end='')
    print_nodes(nodes)
    for n in nodes:
        states[0].append(n[0])
    for i in range(steps):
        nodes = step(nodes)
        if i % print_every == 0:
            print(str(i + 1) + ': ', end='')
            print_nodes(nodes)
        state = []
        for n in nodes:
           state.append(n[0]) 
        states.append(state)
    print_attractor(states)

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
            new_start_state[i] = not new_start_state[i]
            new_nodes = []
            for j in range(0, N):
                new_nodes.append((new_start_state[j], nodes[j][1], nodes[j][2]))
            step_loop(new_nodes, steps, print_every)

if __name__ == "__main__":
    main()
