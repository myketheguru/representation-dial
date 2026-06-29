# artifact-version: 1.0.0
"""incompressibility.py -- does a NEW representation always help? Test the same
Boolean functions across SEVERAL representations:
  minterms (DNF magnitude) | ANF monomials (polynomial/GF2) | ROBDD nodes (branching)
Structured functions should be TINY in their MATCHED representation (huge in others)
-- that is the FFT/suffix-tree phenomenon, representation matters. RANDOM functions
should be EXPONENTIAL in ALL representations -- a representation-INDEPENDENT floor
(the counting/incompressibility argument: not enough small descriptions to go round,
true for present AND future representations).
Run: python incompressibility.py"""
import random
rng = random.Random(0)


def anf_monomials(tt, n):
    a = list(tt)
    for i in range(n):                       # fast Mobius transform over GF(2)
        b = 1 << i
        for mask in range(1 << n):
            if mask & b:
                a[mask] ^= a[mask ^ b]
    return sum(a)


def robdd_nodes(tt):
    memo = {}; internal = set()
    def build(s):
        if s in memo:
            return memo[s]
        if len(s) == 1:
            cid = ('L', s[0])
        else:
            h = len(s) // 2
            lo = build(s[:h]); hi = build(s[h:])
            cid = lo if lo == hi else ('N', lo, hi)   # reduction rule
            if lo != hi:
                internal.add(cid)
        memo[s] = cid
        return cid
    build(tuple(tt))
    return len(internal)


def funcs(n):
    N = 1 << n
    pc = [bin(i).count("1") for i in range(N)]
    fs = {
        "AND":      [1 if i == N - 1 else 0 for i in range(N)],
        "OR":       [1 if i > 0 else 0 for i in range(N)],
        "PARITY":   [pc[i] & 1 for i in range(N)],
        "MAJORITY": [1 if pc[i] > n // 2 else 0 for i in range(N)],
    }
    for k in range(3):
        fs[f"RANDOM{k+1}"] = [rng.randint(0, 1) for _ in range(N)]
    return fs


def main():
    print("=== Does a new representation always help? size across representations ===")
    print("(structured = small in its MATCHED representation; random = large in ALL)\n")
    for n in [8, 10, 12]:
        print(f"n={n}  (truth table = {1<<n} bits)   "
              f"{'function':10s} {'minterms':>9s} {'ANF monos':>10s} {'ROBDD nodes':>12s}")
        for name, tt in funcs(n).items():
            print(f"{'':41s}{name:10s} {sum(tt):>9d} {anf_monomials(tt, n):>10d} {robdd_nodes(tt):>12d}")
        print()
    print("READING:")
    print(" * AND: tiny in EVERY representation (1 minterm, 1 ANF monomial, ~n BDD nodes).")
    print(" * PARITY: HUGE as DNF/minterms (2^(n-1)) but TINY in ANF (n monomials) & BDD (~n).")
    print("   -> representation MATTERS: the matched prior (GF2/ANF) collapses it. (ChatGPT's")
    print("      FFT/suffix-tree point -- correct, and it is exactly 'find the matched prior'.)")
    print(" * RANDOM: ~2^(n-1) minterms, ~2^(n-1) ANF monomials, ~2^n/n BDD nodes -- LARGE in")
    print("   ALL THREE. No representation here is small, and by COUNTING none can be (there")
    print("   are 2^(2^n) functions but far fewer small descriptions in any fixed language).")
    print("\nVERDICT: a new representation helps IFF the function has structure matched to it.")
    print("It REVEALS hidden structure (lowering a naive bound); it cannot MANUFACTURE structure")
    print("that isn't there. The floor for unstructured objects is representation-INDEPENDENT --")
    print("true for future representations too. Conservation holds at the floor; discovery lives")
    print("above it, by finding matched priors for structure we hadn't exploited.")


if __name__ == "__main__":
    main()
