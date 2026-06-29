# artifact-version: 1.0.0
"""causal_compression.py -- compression is CAUSALLY BLIND. Two structural models,
X->Y and Y->X, generate the SAME observational distribution (identical log-likelihood
/ compression) but give OPPOSITE interventional predictions. No amount of compressing
PASSIVE data closes the gap; you must ACT (experiment). This is Pearl's causal
hierarchy in miniature: compression SELECTS explanations, it doesn't GENERATE causal
ones. Run: python causal_compression.py"""
import random, math


def run(N=5000, seed=0):
    rng = random.Random(seed)
    X = [rng.gauss(0, 1) for _ in range(N)]
    Y = [2 * x + rng.gauss(0, 1) for x in X]                  # TRUE model: X -> Y

    def linfit(U, V):
        n = len(U); mu = sum(U) / n; mv = sum(V) / n
        cov = sum((U[i] - mu) * (V[i] - mv) for i in range(n)) / n
        var = sum((U[i] - mu) ** 2 for i in range(n)) / n
        a = cov / var; s2 = sum((V[i] - a * U[i]) ** 2 for i in range(n)) / n
        return a, -0.5 * n * (math.log(2 * math.pi * s2) + 1)

    def gll(U):
        n = len(U); mu = sum(U) / n; s2 = sum((u - mu) ** 2 for u in U) / n
        return -0.5 * n * (math.log(2 * math.pi * s2) + 1)

    _, llf = linfit(X, Y); _, llr = linfit(Y, X)
    fwd = gll(X) + llf      # describe joint as P(X)P(Y|X)  (X->Y)
    rev = gll(Y) + llr      # describe joint as P(Y)P(X|Y)  (Y->X)
    print("OBSERVATIONAL compression / fit (total log-likelihood of the SAME data):")
    print(f"  model X->Y : {fwd:8.1f}")
    print(f"  model Y->X : {rev:8.1f}   -> essentially IDENTICAL ({abs(fwd-rev):.2f} apart)")
    print("  Compression / MDL CANNOT tell the two causal directions apart.\n")
    print("INTERVENTION distinguishes them instantly. Predict E[Y | do(X=3)]:")
    print(f"  true model X->Y : 2*3 = {2*3}")
    print(f"  model Y->X      : X downstream of Y, so do(X) cannot move Y -> E[Y] = {0}")
    print("  Same observations, opposite interventional predictions. Causality > compression.")


if __name__ == "__main__":
    run()
