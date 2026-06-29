"""access_search_split_v4.py -- Project A, version 4.0.0 (the definitive structure sweep).

v3 fixed the tooling (rank metric + clipped training) and resolved the DIMENSION question on a
pure tree. v4 closes the loop by re-running the STUDY'S PRIMARY pre-registered design -- the
structure-knob sweep -- with that trustworthy tooling. At dim=2 (where the hyperbolic edge is
largest), sweep structure from a pure tree (struct=1.0) to random (struct=0.0) and measure the
hyperbolic MAP/MRR gap. Prediction: the gap is positive for hierarchy and shrinks to ~0 as the
structure is destroyed -- "matched geometry helps exactly to the extent the structure is there."

Reuses v1's gen_graph and v3's train_v3 + rank_metrics unchanged. Pure numpy.
Run (from this folder): python access_search_split_v4.py

version: 4.0.0  (v1 structure sweep w/ top-1 metric; v3 dimension sweep w/ rank metric; v4 =
                 structure sweep w/ the rank metric -- the definitive primary result)
"""
import numpy as np
from access_search_split import gen_graph
from access_search_split_v3 import train_v3, rank_metrics


def main():
    n, b, dim, reps, epochs = 150, 3, 2, 2, 150
    print(f"=== access/search split v4: STRUCTURE sweep at dim={dim}, RANK metric, n={n}, reps={reps} ===")
    print(f"{'struct(1-q)':>11s} | {'MAP Euc':>8s} {'MAP Poin':>9s} {'gapMAP':>7s} | {'gapMRR':>7s}")
    for q in (0.0, 0.2, 0.4, 0.7, 1.0):
        me, mp, rg = [], [], []
        for r in range(reps):
            g = np.random.default_rng(100 * r + int(q * 10))
            _, nbrs = gen_graph(n, b, q, g)
            Xe = train_v3(nbrs, n, dim, "euclid", np.random.default_rng(7 + r), epochs=epochs)
            Xp = train_v3(nbrs, n, dim, "poincare", np.random.default_rng(7 + r), epochs=epochs)
            ae, ce = rank_metrics(Xe, nbrs, "euclid")
            ap, cp = rank_metrics(Xp, nbrs, "poincare")
            me.append(ae); mp.append(ap); rg.append(cp - ce)
        print(f"{1-q:>11.2f} | {np.mean(me):>8.3f} {np.mean(mp):>9.3f} {np.mean(mp)-np.mean(me):>+7.3f} | "
              f"{np.mean(rg):>+7.3f}", flush=True)
    print("\nREAD: at dim=2 with the trustworthy rank metric, the hyperbolic MAP gap should be POSITIVE")
    print("for hierarchy (struct~1.0) and SHRINK toward 0 as structure is destroyed (struct~0.0) -- the")
    print("original pre-registered hypothesis, now with a metric we trust: matched geometry helps")
    print("exactly to the extent the structure is there.")


if __name__ == "__main__":
    main()
