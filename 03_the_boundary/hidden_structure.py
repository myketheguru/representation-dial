# artifact-version: 1.0.0
"""hidden_structure.py -- low effective DOF is NECESSARY but NOT SUFFICIENT for
efficient computation/discovery. Three strings: A = hidden low-DOF (fully determined
by a 32-bit seed, cryptographically expanded), B = visible low-DOF (periodic), C =
truly random. To a standard structure-exploiter (gzip), A and C are indistinguishable
(both incompressible) -- yet A has only 32 bits of true DOF. The constraint must be
computationally ACCESSIBLE; the A-vs-B gap is exactly cryptography / one-way functions.
Run: python hidden_structure.py"""
import hashlib, zlib, random


def run(N=20000, seed=0xDEADBEEF):
    rng = random.Random(0)
    A = b"".join(hashlib.sha256(seed.to_bytes(4, "big") + i.to_bytes(4, "big")).digest() for i in range(N // 32))
    B = (b"THE-STRUCTURE-IS-VISIBLE-" * (N // 25 + 1))[:len(A)]
    C = bytes(rng.randrange(256) for _ in range(len(A)))
    ratio = lambda s: len(zlib.compress(s, 9)) / len(s)
    print(f"{'string':34s} {'true DOF':>14s} {'gzip ratio':>11s}")
    print(f"{'A hidden low-DOF (hash-expanded)':34s} {'~32 bits':>14s} {ratio(A):>11.3f}")
    print(f"{'B visible low-DOF (periodic)':34s} {'~few bits':>14s} {ratio(B):>11.3f}")
    print(f"{'C truly random':34s} {'~full':>14s} {ratio(C):>11.3f}")
    print("\nA and C are INDISTINGUISHABLE to a standard structure-exploiter (gzip ~1.0),")
    print("yet A has 32 bits of true DOF and C has ~full. A's low DOF is REAL but HIDDEN.")
    print("=> low effective DOF is NECESSARY but NOT SUFFICIENT; the constraint must also be")
    print("   computationally ACCESSIBLE. The gap A-vs-B (same low DOF, opposite visibility) is")
    print("   exactly cryptography / one-way functions -- structure that exists but can't be found.")


if __name__ == "__main__":
    run()
