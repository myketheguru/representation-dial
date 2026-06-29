# artifact-version: 1.0.0
"""structured_np.py -- the structured-NP sub-question, to its limit.

Schaefer's dichotomy: a Boolean CSP is either in P (via a specific structural
algebra) or NP-complete -- a knife-edge, no middle ground. We demonstrate it:
problems that look IDENTICAL on the surface (clauses of 3 literals) but differ in
ALGEBRAIC structure, and show (1) structure -- not size -- decides whether search
collapses to direct computation, and (2) the collapse happens ONLY with the algebra
MATCHED to the structure (find-the-right-prior).

  XOR-SAT (linear over GF(2))  -- Gaussian elimination = DIRECT, polynomial, no search
                               -- the SAME instance under DPLL (general search) EXPLODES
  3-SAT   (Boolean OR)         -- no matched poly algebra (NP-complete); DPLL EXPLODES
  2-SAT   (implication)        -- SCC = DIRECT, linear (a different matched algebra)
Run: python structured_np.py
"""
import sys, time, random, collections
sys.setrecursionlimit(100000)
rng = random.Random(1)


def rand_3regular(V):
    """Random 3-regular graph (configuration model) -- an expander whp."""
    while True:
        stubs = [v for v in range(V) for _ in range(3)]
        rng.shuffle(stubs)
        edges = set(); ok = True
        for i in range(0, len(stubs), 2):
            a, b = stubs[i], stubs[i + 1]
            e = (min(a, b), max(a, b))
            if a == b or e in edges:
                ok = False; break
            edges.add(e)
        if ok and len(edges) == 3 * V // 2:
            return list(edges)


def tseitin(V):
    """Provably DPLL/resolution-exponential parity formula on a 3-regular expander:
    edge=var, vertex=XOR(incident edges)=charge, total charge ODD -> UNSAT.
    Returns (xor_eqs over E vars, CNF). Gaussian proves UNSAT instantly."""
    edges = rand_3regular(V)
    eid = {e: i for i, e in enumerate(edges)}
    inc = collections.defaultdict(list)
    for e in edges:
        inc[e[0]].append(eid[e]); inc[e[1]].append(eid[e])
    eqs, cnf = [], []
    for v in range(V):
        vs = inc[v]; mask = 0
        for vi in vs:
            mask |= (1 << vi)
        rhs = 1 if v == 0 else 0                      # one odd vertex -> total odd -> UNSAT
        eqs.append((mask, rhs))
        for bits in range(1 << len(vs)):
            if bin(bits).count("1") % 2 != rhs:
                cnf.append(tuple((-(vi + 1) if (bits >> i) & 1 else (vi + 1)) for i, vi in enumerate(vs)))
    return eqs, cnf, len(edges)


# ---------- XOR-SAT via Gaussian elimination over GF(2) (the matched algebra) ----------
def gf2_solve(eqs):
    """eqs: list of (mask:int over vars, rhs:0/1). Returns ('SAT'|'UNSAT', row_ops)."""
    basis = {}; ops = 0
    for m, r in eqs:
        while m:
            lb = m & (-m)
            if lb in basis:
                bm, br = basis[lb]; m ^= bm; r ^= br; ops += 1
            else:
                basis[lb] = (m, r); break
        else:
            if r == 1:
                return "UNSAT", ops
    return "SAT", ops


def rand_xor(n, m, k=3):
    eqs = []
    for _ in range(m):
        vs = rng.sample(range(n), k)
        mask = 0
        for v in vs:
            mask |= (1 << v)
        eqs.append((mask, rng.randint(0, 1)))
    return eqs


def xor_to_cnf(eqs, k=3):
    """Each XOR eq -> 2^(k-1) CNF clauses (forbid the wrong-parity assignments)."""
    clauses = []
    for mask, rhs in eqs:
        vs = [i for i in range(mask.bit_length()) if (mask >> i) & 1]
        for bits in range(1 << len(vs)):
            if bin(bits).count("1") % 2 != rhs:
                clauses.append(tuple((-(v + 1) if (bits >> i) & 1 else (v + 1))
                                     for i, v in enumerate(vs)))
    return clauses


# ---------- DPLL (general search -- the UNMATCHED algebra for XOR) ----------
def dpll(clauses, n, budget=400000):
    dec = [0]
    def go(clauses, assign):
        cs = []
        for c in clauses:
            nc = []; sat = False
            for lit in c:
                v = abs(lit); val = assign.get(v)
                if val is None:
                    nc.append(lit)
                elif (lit > 0) == val:
                    sat = True; break
            if sat:
                continue
            if not nc:
                return False
            cs.append(nc)
        units = [c[0] for c in cs if len(c) == 1]
        if units:
            a = dict(assign)
            for u in units:
                v = abs(u); val = u > 0
                if a.get(v) is None:
                    a[v] = val
                elif a[v] != val:
                    return False
            return go(cs, a)
        if not cs:
            return True
        if dec[0] > budget:
            raise TimeoutError
        v = abs(cs[0][0]); dec[0] += 1
        for val in (True, False):
            a = dict(assign); a[v] = val
            if go(cs, a):
                return True
        return False
    try:
        res = go([list(c) for c in clauses], {})
        return ("SAT" if res else "UNSAT"), dec[0], False
    except TimeoutError:
        return "?", dec[0], True


def rand_3sat(n, m):
    cl = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), 3)
        cl.append(tuple(v if rng.random() < 0.5 else -v for v in vs))
    return cl


# ---------- 2-SAT via implication-graph SCC (a different matched algebra) ----------
def twosat(n, clauses):
    """clauses: list of (lit,lit). vars 1..n. Returns ('SAT'|'UNSAT', time)."""
    t0 = time.time()
    N = 2 * n
    def idx(lit):
        v = abs(lit) - 1
        return 2 * v + (0 if lit > 0 else 1)
    def neg(i):
        return i ^ 1
    g = [[] for _ in range(N)]; gr = [[] for _ in range(N)]
    for a, b in clauses:
        ia, ib = idx(a), idx(b)
        g[neg(ia)].append(ib); g[neg(ib)].append(ia)
        gr[ib].append(neg(ia)); gr[ia].append(neg(ib))
    order = []; vis = [False] * N
    for s in range(N):
        if vis[s]:
            continue
        stack = [(s, 0)]
        while stack:
            node, pi = stack.pop()
            if pi == 0:
                if vis[node]:
                    continue
                vis[node] = True
            if pi < len(g[node]):
                stack.append((node, pi + 1))
                if not vis[g[node][pi]]:
                    stack.append((g[node][pi], 0))
            else:
                order.append(node)
    comp = [-1] * N; c = 0
    for node in reversed(order):
        if comp[node] != -1:
            continue
        stack = [node]; comp[node] = c
        while stack:
            u = stack.pop()
            for w in gr[u]:
                if comp[w] == -1:
                    comp[w] = c; stack.append(w)
        c += 1
    for v in range(n):
        if comp[2 * v] == comp[2 * v + 1]:
            return "UNSAT", time.time() - t0
    return "SAT", time.time() - t0


def rand_2sat(n, m):
    return [(rng.choice([1, -1]) * rng.randint(1, n), rng.choice([1, -1]) * rng.randint(1, n))
            for _ in range(m)]


def main():
    print("=== Structured-NP collapse: structure (not size) decides; matched prior required ===\n")
    print("--- XOR-SAT, Gaussian (matched algebra) scales POLYNOMIALLY (m=1.1n, over-constrained) ---")
    print(f"  {'n':>6s} {'GF2 row-ops':>12s} {'GF2 time':>9s} {'result':>7s}")
    for n in [100, 500, 1000, 3000, 8000]:
        eqs = rand_xor(n, int(1.1 * n))
        t = time.time(); res, ops = gf2_solve(eqs); tg = time.time() - t
        print(f"  {n:>6d} {ops:>12d} {tg:>8.3f}s {res:>7s}")

    print("\n--- THE SAME parity problem, two algebras (Tseitin formula on a 3-regular expander) ---")
    print("    matched=Gaussian (instant UNSAT) vs unmatched=DPLL (provably exponential)")
    print(f"  {'V':>4s} {'#vars E':>8s} | {'GF2 ops':>8s} {'GF2 time':>9s} | {'DPLL decisions':>16s} {'DPLL time':>10s}")
    for V in [10, 20, 30, 40, 50]:
        eqs, cnf, E = tseitin(V)
        t = time.time(); rg, ops = gf2_solve(eqs); tg = time.time() - t
        t = time.time(); _, dec, blew = dpll(cnf, E, budget=150000); td = time.time() - t
        dd = f">{dec} (exploded)" if blew else str(dec)
        print(f"  {V:>4d} {E:>8d} | {ops:>8d} {tg:>8.3f}s | {dd:>16s} {td:>9.2f}s   (GF2={rg})")

    print("\n--- 3-SAT (Boolean OR, NP-complete) at critical alpha=4.27: DPLL EXPLODES (no matched algebra) ---")
    print(f"  {'n':>4s} {'DPLL decisions':>16s} {'time':>8s}")
    for n in [40, 60, 80, 100]:
        cl = rand_3sat(n, int(4.27 * n))
        t = time.time(); res, dec, blew = dpll(cl, n, budget=120000); td = time.time() - t
        dd = f">{dec} (exploded)" if blew else f"{dec} ({res})"
        print(f"  {n:>4d} {dd:>16s} {td:>7.2f}s")

    print("\n--- 2-SAT (2 literals, implication, P): SCC (a different matched algebra) ---")
    print(f"  {'n':>6s} {'result':>7s} {'time':>9s}")
    for n in [1000, 10000, 100000]:
        res, tt = twosat(n, rand_2sat(n, 3 * n))
        print(f"  {n:>6d} {res:>7s} {tt:>8.3f}s")

    print("\nVERDICT: XOR-SAT and 3-SAT are surface-identical (3-literal clauses) but XOR")
    print("collapses to DIRECT polynomial computation -- ONLY via Gaussian (the matched")
    print("linear-algebra prior); the SAME XOR explodes under general DPLL search, and")
    print("3-SAT explodes with no matched poly algebra at all. 2-SAT collapses via yet")
    print("another matched algebra (SCC). Schaefer's dichotomy: these structured cases are")
    print("PROVABLY the only collapsible ones -- a knife-edge. The collapse is real but is a")
    print("PRIOR matched to structure, never a universal solvent. (find the right prior.)")


if __name__ == "__main__":
    main()
