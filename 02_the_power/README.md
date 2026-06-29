# 02 · The power — structured search collapses, under the matched prior

**Question:** if arbitrary search is conserved, can a representation collapse *structured* search?
**Answer:** yes — but only with the algebra **matched** to the structure, on a proven knife-edge.

| artifact (version) | what it tests | the result |
|---|---|---|
| `structured_np.py` (1.0.0) | Does the matched algebra collapse a problem the mismatched one explodes on? (Schaefer's dichotomy; XOR-SAT vs 3-SAT; Tseitin parity) | The **same** parity formula: Gaussian elimination proves it instantly; general DPLL search explodes (decisions → >150,000). Matched prior = instant, mismatched = exponential. 2-SAT collapses via a *different* matched algebra (SCC); 3-SAT, with none, stays hard. |
| `fourier_alignment.py` (1.0.0) | Does the Fourier basis diagonalize a convolution (aligned structure) but do nothing for a random operator? | Convolution → off-diagonal energy **0.0000** (diagonal); random operator → **0.97** (untouched). The FFT basis is the cyclic group's irreducible representations — alignment with symmetry. |

**Run:** `python structured_np.py` · `python fourier_alignment.py` (pure Python).

**Takeaway:** the collapse is real but is always a *prior matched to a specific structure*, never a
universal trick. A representation simplifies a problem exactly when it aligns the free operations with
the structure the problem already has. *Established — Schaefer's dichotomy, harmonic analysis /
geometric deep learning — reproduced here.*
