"""access_search_split.py -- Project A (STUDY_access_search_split.md).

Does matched geometry move the ACCESS/SEARCH boundary? Embed a graph whose hierarchy we
control (a tree, rewired by fraction q toward random) in Euclidean R^k and in the Poincare
ball H^k, matched k/budget. ACCESS FRACTION = fraction of nodes whose nearest neighbour in
the embedding is a true graph-neighbour (answer reachable by cheap geometric access, no
search). Hypothesis: hyperbolic > Euclidean for hierarchy, gap shrinks as q->1 (structure
gone), both -> chance (the curse-of-dimensionality floor).

Replicates the known core (Nickel & Kiela 2017: hyperbolic embeds hierarchy better). The
contribution is the access/search-split framing + the structure-knob sweep + the floor.
Pure numpy, hand-rolled Riemannian SGD. Run: python access_search_split.py

version: 1.0.0  -- the STRUCTURE-KNOB sweep at fixed dim=5.
See access_search_split_v2.py (v2.0.0) for the DIMENSION sweep (the run-1 confound check).
"""
import numpy as np

EPS = 1e-9


# ---------- geometry: distance + gradient of d(u,v) w.r.t. u ----------
def dist(u, v, geom):
    if geom == "euclid":
        return np.linalg.norm(u - v)
    du = 1 - np.dot(u, u); dv = 1 - np.dot(v, v)
    x = 1 + 2 * np.dot(u - v, u - v) / (max(du, EPS) * max(dv, EPS))
    return np.arccosh(max(x, 1 + EPS))


def grad_d(u, v, geom):
    """Euclidean gradient d d(u,v)/d u."""
    if geom == "euclid":
        diff = u - v
        return diff / (np.linalg.norm(diff) + EPS)
    a = 1 - np.dot(u, u); b = 1 - np.dot(v, v)
    g = np.dot(u - v, u - v)
    gamma = 1 + 2 * g / (max(a, EPS) * max(b, EPS))
    s = np.sqrt(max(gamma * gamma - 1, EPS))
    coef = 4 / (max(b, EPS) * s)
    return coef * (((np.dot(v, v) - 2 * np.dot(u, v) + 1) / (max(a, EPS) ** 2)) * u - v / max(a, EPS))


def project(X):
    n = np.linalg.norm(X, axis=1, keepdims=True)
    mask = (n >= 1).ravel()
    X[mask] = X[mask] / n[mask] * (1 - 1e-5)
    return X


# ---------- data: tree with a structure knob ----------
def gen_graph(n, b, q, rng):
    edges = [((c - 1) // b, c) for c in range(1, n)]                  # balanced tree
    out = []
    for (u, v) in edges:
        if rng.random() < q:                                          # rewire toward random
            a = rng.integers(n); c = rng.integers(n)
            while c == a:
                c = rng.integers(n)
            out.append((int(a), int(c)))
        else:
            out.append((u, v))
    nbrs = [set() for _ in range(n)]
    for u, v in out:
        if u != v:
            nbrs[u].add(v); nbrs[v].add(u)
    return out, nbrs


# ---------- train embeddings (softmax over negatives, Riemannian SGD) ----------
def train(nbrs, n, dim, geom, rng, epochs=200, lr=0.3, nneg=8):
    X = rng.standard_normal((n, dim)) * 1e-3
    pos = [(u, v) for u in range(n) for v in nbrs[u] if u < v]
    for ep in range(epochs):
        lr_e = lr * (0.1 if ep < 10 else 1.0)                         # burn-in
        rng.shuffle(pos)
        for u, v in pos:
            cand = [v]
            while len(cand) < 1 + nneg:
                w = int(rng.integers(n))
                if w != u and w not in nbrs[u]:
                    cand.append(w)
            d = np.array([dist(X[u], X[c], geom) for c in cand])
            p = np.exp(-d - (-d).max()); p /= p.sum()                 # softmax over -dist
            gu = np.zeros(dim)
            for i, c in enumerate(cand):
                gd_u = grad_d(X[u], X[c], geom)
                gd_c = grad_d(X[c], X[u], geom)
                coef = (1.0 - p[i]) if i == 0 else (-p[i])            # dLoss/dscore sign
                # Loss=-log p(v): dL/du = gd(u,v) - sum p_i gd(u,c_i); dL/dc as below
                gu += (gd_u if i == 0 else 0) - p[i] * gd_u
                gc = (1 - p[0]) * gd_c if i == 0 else -p[i] * gd_c
                if geom == "poincare":
                    gc *= ((1 - np.dot(X[c], X[c])) ** 2) / 4
                X[c] -= lr_e * gc
            if geom == "poincare":
                gu *= ((1 - np.dot(X[u], X[u])) ** 2) / 4
            X[u] -= lr_e * gu
            if geom == "poincare":
                project(X)
    return X


# ---------- access fraction ----------
def pairwise(X, geom):
    if geom == "euclid":
        d = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)
        return d
    nn = np.sum(X * X, axis=1)
    sq = np.sum((X[:, None, :] - X[None, :, :]) ** 2, axis=2)
    denom = np.outer(1 - nn, 1 - nn)
    arg = 1 + 2 * sq / np.clip(denom, EPS, None)
    return np.arccosh(np.clip(arg, 1 + EPS, None))


def access_fraction(X, nbrs, geom):
    D = pairwise(X, geom); np.fill_diagonal(D, np.inf)
    nn = D.argmin(1)
    return np.mean([nn[u] in nbrs[u] for u in range(len(nbrs)) if nbrs[u]])


def main():
    rng = np.random.default_rng(0)
    n, b, dim, reps = 300, 3, 5, 2
    print(f"=== access/search split v1: STRUCTURE sweep, n={n} tree(b={b}) dim={dim} ===")
    print(f"{'q (1-q=structure)':>18s} {'Euclid access':>14s} {'Poincare access':>16s} {'gap(P-E)':>9s} {'chance':>7s}")
    for q in (0.0, 0.2, 0.4, 0.7, 1.0):
        eu, po, ch = [], [], []
        for r in range(reps):
            g = np.random.default_rng(100 * r + int(q * 10))
            _, nbrs = gen_graph(n, b, q, g)
            deg = np.mean([len(s) for s in nbrs])
            ch.append(deg / (n - 1))
            eu.append(access_fraction(train(nbrs, n, dim, "euclid", np.random.default_rng(7 + r)), nbrs, "euclid"))
            po.append(access_fraction(train(nbrs, n, dim, "poincare", np.random.default_rng(7 + r)), nbrs, "poincare"))
        e, p, c = np.mean(eu), np.mean(po), np.mean(ch)
        print(f"{1-q:>18.2f} {e:>14.3f} {p:>16.3f} {p-e:>+9.3f} {c:>7.3f}")
    print("\nREAD: if Poincare>Euclid at high structure (q=0) and the gap shrinks toward q=1,")
    print("matched geometry moves the access boundary, bounded by structure. If gap~0 throughout,")
    print("null. chance = avg-degree/(n-1) is the curse-of-dimensionality floor.")


if __name__ == "__main__":
    main()
