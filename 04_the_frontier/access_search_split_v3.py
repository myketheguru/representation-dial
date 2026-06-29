"""access_search_split_v3.py -- Project A, version 3.0.0 (the rebuild).

v2 (dimension sweep) came back INCONCLUSIVE: it contradicted the established result, which we
judged an *implementation* fault, not geometry. v3 fixes the two suspects:
  (1) METRIC: top-1 access is brittle (crowding-sensitive). v3 uses RANK-based reconstruction
      metrics -- MAP and mean reciprocal rank (MRR) -- the standard for embedding quality
      (Nickel & Kiela 2017). Higher = better.
  (2) TRAINING: gradient CLIPPING (stops boundary blow-up in the Poincare ball), an lr DECAY
      schedule, and more epochs -- so 2D hyperbolic actually converges.
Reuses v1's geometry primitives (dist/grad/project/gen_graph/pairwise) unchanged. Pure numpy.
Run (from this folder): python access_search_split_v3.py

version: 3.0.0  (see v1 = structure sweep, v2 = dimension sweep w/ top-1 metric)
"""
import numpy as np
from access_search_split import dist, grad_d, project, gen_graph, pairwise


def train_v3(nbrs, n, dim, geom, rng, epochs=350, lr=0.5, nneg=10, clip=1.0):
    X = rng.standard_normal((n, dim)) * 1e-3
    pos = [(u, v) for u in range(n) for v in nbrs[u] if u < v]
    for ep in range(epochs):
        lr_e = lr * (0.1 if ep < 20 else max(0.05, 1.0 - ep / epochs))      # burn-in + linear decay
        rng.shuffle(pos)
        for u, v in pos:
            cand = [v]
            while len(cand) < 1 + nneg:
                w = int(rng.integers(n))
                if w != u and w not in nbrs[u]:
                    cand.append(w)
            d = np.array([dist(X[u], X[c], geom) for c in cand])
            p = np.exp(-d - (-d).max()); p /= p.sum()
            gu = grad_d(X[u], X[cand[0]], geom).copy()                       # dL/du = g(u,v) - sum p_i g(u,c_i)
            for i, c in enumerate(cand):
                gu -= p[i] * grad_d(X[u], X[c], geom)
                gc = (1 - p[0]) * grad_d(X[c], X[u], geom) if i == 0 else -p[i] * grad_d(X[c], X[u], geom)
                nc = np.linalg.norm(gc)
                if nc > clip:
                    gc = gc / nc * clip
                if geom == "poincare":
                    gc *= ((1 - np.dot(X[c], X[c])) ** 2) / 4
                X[c] -= lr_e * gc
            ng = np.linalg.norm(gu)
            if ng > clip:
                gu = gu / ng * clip
            if geom == "poincare":
                gu *= ((1 - np.dot(X[u], X[u])) ** 2) / 4
            X[u] -= lr_e * gu
            if geom == "poincare":
                project(X)
    return X


def rank_metrics(X, nbrs, geom):
    """MAP and MRR of reconstructing each node's true neighbours by embedding distance."""
    D = pairwise(X, geom); np.fill_diagonal(D, np.inf)
    n = len(nbrs)
    order = np.argsort(D, axis=1)
    rankpos = np.empty((n, n), dtype=int)
    for u in range(n):
        rankpos[u, order[u]] = np.arange(n)
    AP, RR = [], []
    for u in range(n):
        if not nbrs[u]:
            continue
        rs = sorted(int(rankpos[u, v]) for v in nbrs[u])                    # 0-indexed ranks of neighbours
        AP.append(np.mean([(k + 1) / (r + 1) for k, r in enumerate(rs)]))   # average precision
        RR.append(1.0 / (rs[0] + 1))                                        # reciprocal rank of nearest nbr
    return float(np.mean(AP)), float(np.mean(RR))


def main():
    n, b, reps, epochs = 200, 3, 2, 200
    print(f"=== access/search split v3: RANK metrics + clipped training, n={n} PURE TREE, reps={reps} ===")
    print(f"{'dim':>4s} | {'MAP Euc':>8s} {'MAP Poin':>9s} {'gapMAP':>7s} | {'MRR Euc':>8s} {'MRR Poin':>9s} {'gapMRR':>7s}")
    for dim in (2, 5, 10):
        me, mp, re_, rp = [], [], [], []
        for r in range(reps):
            g = np.random.default_rng(100 * r)
            _, nbrs = gen_graph(n, b, 0.0, g)                     # pure tree = the decisive case
            Xe = train_v3(nbrs, n, dim, "euclid", np.random.default_rng(7 + r), epochs=epochs)
            Xp = train_v3(nbrs, n, dim, "poincare", np.random.default_rng(7 + r), epochs=epochs)
            a, c = rank_metrics(Xe, nbrs, "euclid"); me.append(a); re_.append(c)
            a, c = rank_metrics(Xp, nbrs, "poincare"); mp.append(a); rp.append(c)
        print(f"{dim:>4d} | {np.mean(me):>8.3f} {np.mean(mp):>9.3f} {np.mean(mp)-np.mean(me):>+7.3f} | "
              f"{np.mean(re_):>8.3f} {np.mean(rp):>9.3f} {np.mean(rp)-np.mean(re_):>+7.3f}", flush=True)
    print("\nREAD: on a pure tree, with a rank metric + converged training, hyperbolic should BEAT")
    print("Euclidean (positive gapMAP/gapMRR), with the largest edge at dim=2. That would confirm the")
    print("v2 inconclusive result was an implementation artifact (brittle top-1 metric + undertrained 2D).")


if __name__ == "__main__":
    main()
