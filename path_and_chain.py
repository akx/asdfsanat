from networkx import Graph, all_simple_paths, chain_decomposition
from tqdm import tqdm


def load_graph():
    g = Graph()
    for file in ["example_out/out-prefix.txt", "example_out/out-suffix.txt"]:
        with open(file, "r") as infp:
            for line in infp:
                line = line.strip()
                if line:
                    a, b = line.split(None, 1)
                    g.add_edge(a, b)
    return g


def find_paths(g):
    # Find all the nodes with only one neighbor
    terminal_nodes = [node for node in g.nodes if g.degree[node] == 1]
    # Further filter these nodes to those that are not terminal, to avoid iterating
    # over simple two-pairs of nodes; we already know they aren't going to be long.
    connected_terminal_nodes = [node for node in terminal_nodes if g.degree[next(g.neighbors(node))] > 1]
    paths = []
    for n1 in tqdm(connected_terminal_nodes):
        for n2 in connected_terminal_nodes:
            for pth in all_simple_paths(g, n1, n2):
                paths.append((n1, n2, pth))
    for n1, n2, path in sorted(paths):
        print(n1, n2, len(path), ' '.join(path))
    print("-" * 80)
    print(max(paths, key=lambda x: len(x[2])))
    print("-" * 80)


def find_chains(g):
    for chain in chain_decomposition(g):
        print(' '.join(f'{a}-{b}' for (a, b) in chain))


g = load_graph()
print("# Paths")
find_paths(g)
print("# Chains")
find_chains(g)
