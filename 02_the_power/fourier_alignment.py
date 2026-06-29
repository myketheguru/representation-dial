# artifact-version: 1.0.0
"""fourier_alignment.py -- a representation simplifies a problem IFF it aligns the
model's free operations with the problem's conserved structure. The FFT basis = the
irreducible representations of the cyclic group Z_n; it diagonalizes ANY convolution
(that IS the structure) and does nothing for a structureless operator.
Pure-Python complex DFT, n=32. Run: python fourier_alignment.py"""
import cmath, random


def run(n=32, seed=0):
    rng = random.Random(seed)
    w = cmath.exp(-2j * cmath.pi / n)
    F = [[w ** (j * k) / (n ** 0.5) for k in range(n)] for j in range(n)]      # DFT basis
    Fh = [[F[k][j].conjugate() for k in range(n)] for j in range(n)]           # conj transpose
    mm = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

    def offdiag(M):
        tot = sum(abs(M[i][j]) ** 2 for i in range(n) for j in range(n))
        dia = sum(abs(M[i][i]) ** 2 for i in range(n))
        return 1 - dia / tot

    c = [rng.gauss(0, 1) for _ in range(n)]
    C = [[c[(j - i) % n] for j in range(n)] for i in range(n)]                 # circulant = convolution
    R = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]               # random (no symmetry)
    print(f"convolution operator, in the Fourier basis:  off-diagonal energy = {offdiag(mm(mm(F,C),Fh)):.4f}  -> DIAGONAL")
    print(f"random      operator, in the Fourier basis:  off-diagonal energy = {offdiag(mm(mm(F,R),Fh)):.4f}  -> not helped")
    print("\nThe FFT basis = the irreducible representations of the cyclic group. It diagonalizes")
    print("ANY convolution (that IS the structure) and does nothing for a structureless operator.")


if __name__ == "__main__":
    run()
