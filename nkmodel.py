import random
import sys
import argparse
from collections import Counter

class Network:
    def __init__(self, n, k, start_state=[], start_conns=[], start_funcs=[]):
        self.nodes = [] 
        self.start_conns = []
        if start_conns == []:
            for i in range(0, n):
                self.start_conns.append(random.sample([x for x in range(n) if x != i], k))
        else:
            self.start_conns = start_conns

        if start_funcs == []:
            start_funcs = [{} for i in range(n)]

        self.start_state = []
        if start_state == []:
            for i in range(0, n):
                bit = bool(random.getrandbits(1))
                self.start_state.append(bit)
                self.nodes.append((bit, self.start_conns[i], start_funcs[i]))
        else:
            self.start_state = start_state
            for i in range(0, n):
                self.nodes.append((self.start_state[i], self.start_conns[i], start_funcs[i]))
    
        self.states = [[]]
        for n in self.nodes:
            self.states[0].append(n[0])

    def step(self):
        new_nodes = []
        for n in self.nodes: 
            in_bits = sum([1<<i for i, b in enumerate(map(lambda x: self.nodes[x][0], n[1])) if b])
            if in_bits not in n[2]:
                n[2][in_bits] = bool(random.getrandbits(1))
            new_nodes.append((n[2][in_bits], n[1], n[2]))
        self.nodes = new_nodes
        state = []
        for n in self.nodes:
            state.append(n[0]) 
        self.states.append(state)

    def step_loop(self, steps, print_every=1, no_out=False):
        if not no_out:
            print('start: ', end='')
            self.print_nodes()
        for i in range(steps):
            self.step()
            if not no_out:
                if i % print_every == 0:
                    print(str(i + 1) + ': ', end='')
                    self.print_nodes()
    
    def get_start_state(self):
        return self.start_state

    def get_start_conns(self):
        return self.start_conns

    def get_funcs(self):
        funcs = []
        for n in self.nodes:
            funcs.append(n[2])

        return funcs
        
    def get_attractor(self):
        sset = set()
        attract_start = []
        attract_end_index = 0
        num_s = []
        for v in self.states:
            num_s.append(sum([1<<i for i, b in enumerate(v) if b]))

        for i, v in enumerate(num_s):
            if v in sset:
                attract_start = v
                attract_end_index = i
                break;
            else:
                sset.add(v)

        if attract_start == []:
            return ();

        attract_start_index = num_s.index(attract_start)
        attractor = self.states[attract_start_index:attract_end_index]
        attractor = tuple(map(tuple, attractor))

        return attractor

    def print_nodes(self):
        print(''.join(['1' if n[0] else '0' for n in self.nodes]))

def print_state(state):
    print(''.join(['1' if s else '0' for s in state]))

def print_attractor(a):
    if a == ():
        print("No Attractor:")
        return;

    print("Attractor:")
    for i, s in enumerate(a):
        print_state(s)
        print('↓')
    print_state(a[0])
    print('period: ' + str(len(a)))

def main():
    parser = argparse.ArgumentParser(description='NK Model Parameter handler')
    parser.add_argument('-n', dest="N", type=int, required=True)
    parser.add_argument('-k', dest="K", type=int, required=True)    
    parser.add_argument('--steps', '-s', dest="steps", type=int, required=True)
    parser.add_argument('-d', action='store_true')
    parser.add_argument('--print-every', '-p', dest='print_every', type=int, default=1)
    parser.add_argument('-c', action='store_true')
    args = parser.parse_args()
    N = args.N
    K = args.K
    if N < K:
        parser.error("N must be greater than K")
    steps = args.steps
    print_every = args.print_every

    start_network = Network(N, K)
    start_network.step_loop(steps, print_every, args.c)
    start_attractor = start_network.get_attractor()
    neighbor_attractors = []
    if args.d:
        for i in range(N):
            if not args.c:
                print('\nNeighbor ' + str(i+1))
            new_start_state = start_network.get_start_state().copy()
            new_start_state[i] = not new_start_state[i]
            new_network = Network(N, K, new_start_state, start_network.get_start_conns().copy(), start_network.get_funcs())
            new_network.step_loop(steps, print_every, args.c)
            neighbor_attractors.append(new_network.get_attractor())

        counted_attractors = dict(Counter(neighbor_attractors))
        set_attractors = {}

        for i, v in counted_attractors.items():
            if tuple(sorted(i)) not in set_attractors:
                set_attractors[tuple(sorted(i))] = (v, i)
            elif tuple(sorted(i)) in set_attractors:
                set_attractors[tuple(sorted(i))] = (set_attractors[tuple(sorted(i))][0] + v, set_attractors[tuple(sorted(i))][1])
        print('\nStart Attractor:')
        print_attractor(start_attractor)
        print('percentage neighbors: ' + str((set_attractors[tuple(sorted(start_attractor))][0]/N) * 100) + '%')
        print('\nNeighbor Attractors:')
        for i, v in set_attractors.items():
            print_attractor(v[1])
            print(str(v[0]) + ' neighbors\n')

if __name__ == "__main__":
    main()
