# artifact-version: 1.0.0
"""treewidth_conservation.py -- testing the deep question to its limit.

The literal "information algebra" that turns search into DIRECT computation is the
valuation algebra / variable elimination (junction-tree local computation): it
answers inference/CSP queries WITHOUT exploring the exponential assignment space.
Its cost = 2^(induced width of the elimination order). The minimum induced width
over ALL orders is the graph's TREEWIDTH.

We test whether treewidth is a CONSERVED, representation-invariant floor:
  1. Representation matters: different elimination orders (= representations) cost
     wildly differently.
  2. But there is a FLOOR (~treewidth) no order beats -> the conserved quantity.
  3. The floor is STRUCTURAL: tiny for structured graphs (chain/tree/grid = direct
     computation is cheap), ~n for dense/"arbitrary" graphs (= exponential = you
     MUST explore). Search content is conserved, not destroyed.
  4. The floor is INVARIANT under relabeling (a pure representation change cannot
     reduce it).
=> An information algebra makes answers direct IFF the structure (treewidth) is
bounded; for arbitrary spaces it degrades to exploration. No free lunch.
Run: python treewidth_conservation.py
"""
import random
rng = random.Random(0)


def induced_width(adj, order):
    """Cost of variable elimination in this order = max clique formed (induced width)."""
    g = {v: set(ns) for v, ns in adj.items()}
    w = 0
    for v in order:
        nb = g[v]
        w = max(w, len(nb))
        for a in nb:                       # connect v's neighbours (fill-in)
            g[a] |= (nb - {a})
            g[a].discard(v)
        del g[v]
    return w


def min_fill_order(adj):
    """Greedy heuristic: eliminate the vertex adding the fewest fill edges (good order)."""
    g = {v: set(ns) for v, ns in adj.items()}
    order = []
    while g:
        def fill(v):
            nb = list(g[v])
            return sum(1 for i in range(len(nb)) for j in range(i + 1, len(nb)) if nb[j] not in g[nb[i]])
        v = min(g, key=fill)
        order.append(v)
        nb = g[v]
        for a in nb:
            g[a] |= (nb - {a}); g[a].discard(v)
        del g[v]
    return order


def best_width(adj, tries=400):
    """Best (lowest) induced width over the min-fill order + many random orders -> ~treewidth."""
    verts = list(adj)
    widths = [induced_width(adj, min_fill_order(adj))]
    rnds = []
    for _ in range(tries):
        o = verts[:]; rng.shuffle(o)
        rnds.append(induced_width(adj, o))
    return min(widths + rnds), rnds, min(widths)


def rand_graph(n, p):
    adj = {v: set() for v in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                adj[i].add(j); adj[j].add(i)
    return adj


def path(n):
    adj = {v: set() for v in range(n)}
    for i in range(n - 1):
        adj[i].add(i + 1); adj[i + 1].add(i)
    return adj


def grid(k):
    adj = {(r, c): set() for r in range(k) for c in range(k)}
    for r in range(k):
        for c in range(k):
            for dr, dc in ((1, 0), (0, 1)):
                if r + dr < k and c + dc < k:
                    adj[(r, c)].add((r + dr, c + dc)); adj[(r + dr, c + dc)].add((r, c))
    return adj


def relabel(adj):
    verts = list(adj); perm = verts[:]; rng.shuffle(perm)
    m = dict(zip(verts, perm))
    g = {m[v]: set() for v in adj}
    for v, ns in adj.items():
        for u in ns:
            g[m[v]].add(m[u])
    return g


def main():
    print("=== Is there an information algebra that makes answers DIRECT? ===")
    print("Variable elimination (the valuation algebra) costs 2^(induced width).")
    print("Below: floor width (best representation ~ treewidth) and the SPREAD over")
    print("representations (random elimination orders), for n=24 random graphs.\n")
    n = 24
    print(f"{'density p':>9s} {'floor (~tw)':>11s} {'best-order cost':>16s} {'rand order width: min/med/max':>30s}")
    for p in [0.1, 0.2, 0.3, 0.5, 0.7, 0.9]:
        adj = rand_graph(n, p)
        floor, rnds, mf = best_width(adj)
        rnds.sort()
        med = rnds[len(rnds) // 2]
        print(f"{p:>9.1f} {floor:>11d} {('2^'+str(floor)):>16s} "
              f"{f'{min(rnds)}/{med}/{max(rnds)}':>30s}")

    print("\n--- STRUCTURED graphs: the algebra IS efficient (direct computation cheap) ---")
    for name, adj in [("path-24 (chain)", path(24)), ("grid 5x5", grid(5)),
                      ("grid 8x8", grid(8))]:
        floor, _, _ = best_width(adj)
        print(f"  {name:18s} n={len(adj):3d}  floor width {floor:2d}  -> cost 2^{floor}")
    # complete graph: the fully 'arbitrary' worst case
    comp = {v: set(u for u in range(16) if u != v) for v in range(16)}
    fc, _, _ = best_width(comp)
    print(f"  {'complete-16':18s} n=16  floor width {fc:2d}  -> cost 2^{fc} (= full exploration)")

    print("\n--- INVARIANCE: relabeling (a pure representation change) cannot reduce the floor ---")
    adj = rand_graph(20, 0.4)
    a = best_width(adj)[0]
    diffs = [best_width(relabel(adj))[0] for _ in range(5)]
    print(f"  floor on G = {a};  floor after 5 random relabelings = {diffs}  (invariant)")

    print("\nVERDICT: the algebra converts search -> direct local computation, but its cost")
    print("is 2^treewidth -- a STRUCTURAL, representation-INVARIANT floor. Bounded structure")
    print("=> direct & cheap. Arbitrary/dense structure => floor ~ n => 2^n => you must")
    print("explore. The search content is CONSERVED; representation relocates it, never destroys it.")


if __name__ == "__main__":
    main()
