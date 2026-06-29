"""access_search_split_v2.py -- Project A, version 2.0.0.

Builds on v1 (access_search_split.py, the structure-knob sweep at dim=5). v1's run-1 flaw:
hyperbolic's advantage is largest at SMALL embedding dimension, where flat (Euclidean) space
runs out of room for hierarchy; dim=5 was too generous. v2 holds the structure levels fixed
and SWEEPS the dimension, to test whether the geometry gap widens at dim=2.

Reuses v1's machinery (graph generation, training, access metric) unchanged -- only the
experiment driver differs, so the two versions are directly comparable. Pure numpy.
Run: python access_search_split_v2.py

version: 2.0.0  (dimension sweep; see access_search_split.py v1.0.0 for the structure sweep)
"""
import numpy as np
from access_search_split import gen_graph, train, access_fraction


def main():
    n, b, reps = 300, 3, 2
    print(f"=== access/search split v2: DIMENSION sweep, n={n} tree(b={b}) ===")
    print(f"{'dim':>4s} {'struct(1-q)':>11s} {'Euclid':>7s} {'Poincare':>9s} {'gap(P-E)':>9s}")
    for dim in (2, 3, 5, 10):
        for q in (0.0, 0.4):                              # pure tree, and a partly-rewired graph
            eu, po = [], []
            for r in range(reps):
                g = np.random.default_rng(100 * r + int(q * 10))
                _, nbrs = gen_graph(n, b, q, g)
                eu.append(access_fraction(train(nbrs, n, dim, "euclid", np.random.default_rng(7 + r)), nbrs, "euclid"))
                po.append(access_fraction(train(nbrs, n, dim, "poincare", np.random.default_rng(7 + r)), nbrs, "poincare"))
            e, p = np.mean(eu), np.mean(po)
            print(f"{dim:>4d} {1-q:>11.2f} {e:>7.3f} {p:>9.3f} {p-e:>+9.3f}")
    print("\nREAD: hyperbolic's edge should be LARGEST at small dim (dim=2), where flat space runs")
    print("out of room for hierarchy. If gap(P-E) for the tree (struct=1.00) is much bigger at dim=2")
    print("than dim=10, the run-1 dimension confound is confirmed and the geometry effect is real")
    print("but dim-sensitive. Compare directly against v1's dim=5 row.")


if __name__ == "__main__":
    main()
