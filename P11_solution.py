import networkx as nx

from P11_input import INPUT_PRODUCTION

INPUT_TEST1 = '''
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
'''

INPUT_TEST2 = '''
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
'''

# Gemini suggested this algorithm
def count_paths(G, src, tgt):
    assert nx.is_directed_acyclic_graph(G)
    topo_order = list(nx.topological_sort(G))
    result = list()
    path_counts = {node: 0 for node in G.nodes()}
    path_counts[src] = 1
    for u in topo_order:
        if path_counts[u] > 0: # If node u is reachable from the source
            # For each neighbor v of u, add paths to u to v's path count
            for v in G.successors(u): # G.successors(u) gets nodes v where (u, v) is an edge
                path_counts[v] += path_counts[u]
    return path_counts[tgt]

def solve_part1(INPUT):
    G = nx.DiGraph()
    for line in INPUT.strip().splitlines():
        src, tgts = line.split(': ')
        for tgt in tgts.split(' '):
            G.add_edge(src, tgt)
    return count_paths(G, 'you', 'out')

def solve_part2(INPUT):
    G = nx.DiGraph()
    for line in INPUT.strip().splitlines():
        src, tgts = line.split(': ')
        for tgt in tgts.split(' '):
            G.add_edge(src, tgt)
    v1 = count_paths(G, 'svr','fft') * count_paths(G, 'fft', 'dac') * count_paths(G, 'dac', 'out')
    v2 = count_paths(G, 'svr','dac') * count_paths(G, 'dac', 'fft') * count_paths(G, 'fft', 'out')
    return v1, v2, v1+v2


print('Part 1 test:', solve_part1(INPUT_TEST1))
print('part 1 prod:', solve_part1(INPUT_PRODUCTION))

print('Part 2 test:', solve_part2(INPUT_TEST2))
print('part 2 prod:', solve_part2(INPUT_PRODUCTION))
