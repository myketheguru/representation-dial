# Artifact versions

Each demo carries its version in-file (`# artifact-version:` or a `version:` line in the docstring).
Semantic-ish: stable demos are 1.0.0; the active frontier experiment is versioned as it iterates.

| artifact | version | folder | what it tests | status |
|---|---|---|---|---|
| `treewidth_conservation.py` | 1.0.0 | 01_the_limit | Is the variable-elimination cost floor (treewidth) beaten by any elimination order? Is it invariant under relabeling? | stable |
| `incompressibility.py` | 1.0.0 | 01_the_limit | Is a random function small in ANY representation (DNF/ANF/BDD)? Is a structured one small in its matched basis? | stable |
| `structured_np.py` | 1.0.0 | 02_the_power | Does the matched algebra (Gaussian) collapse a parity problem the mismatched one (DPLL) explodes on? Schaefer knife-edge. | stable |
| `fourier_alignment.py` | 1.0.0 | 02_the_power | Does the Fourier basis diagonalize a convolution (aligned structure) but not a random operator? | stable |
| `hidden_structure.py` | 1.0.0 | 03_the_boundary | Can a standard compressor (gzip) tell a hash-expanded low-DOF string from true randomness? | stable |
| `causal_compression.py` | 1.0.0 | 03_the_boundary | Do two opposite causal models fit observations identically yet predict do() oppositely? | stable |
| `access_search_split.py` | 1.0.0 | 04_the_frontier | Does matched (hyperbolic) geometry raise the access fraction, bounded by structure? (structure-knob sweep, dim=5) | active |
| `access_search_split_v2.py` | 2.0.0 | 04_the_frontier | Is the geometry advantage largest at small dimension? (dimension sweep, top-1 metric; the v1 confound check; imports v1) | superseded by v3 |
| `access_search_split_v3.py` | 3.0.0 | 04_the_frontier | The rebuild: rank metric (MAP/MRR) + clipped/converged training. Resolves v2 — hyperbolic beats Euclidean for hierarchy, edge largest at dim=2 (trustworthy) | active |

## Changelog
- **access_search_split 1.0.0** — structure-knob sweep at dim=5. First result: directional (hyperbolic
  gap +0.04..+0.06 for hierarchy, flips negative as structure is destroyed) but modest and confounded
  (tree reconstruction is intrinsically harder; dim=5 too generous).
- **access_search_split_v2 2.0.0** — dimension sweep, holding structure fixed, to isolate the v1
  dimension confound. Reuses v1's machinery unchanged. **Result: INCONCLUSIVE** — predicted hyperbolic's
  edge largest at dim=2, but for the tree the gap is *negative* at dim=2 (−0.100) and positive only at
  dim≥5. Contradicts the established Nickel–Kiela finding ⇒ likely an *implementation* fault (undertrained
  2D Riemannian SGD + a crowding-sensitive top-1 metric), not geometry. Needs a proper hyperbolic
  optimizer + a rank-based metric before the question can be answered.
- **access_search_split_v3 3.0.0** — the rebuild. Rank-based metric (MAP + MRR, not top-1) + clipped,
  converged training. On a pure tree: hyperbolic beats Euclidean at every dim, edge largest at dim=2
  (MAP gap +0.079 → +0.003 from dim 2 → 10). The established Nickel–Kiela pattern. **Resolves v2: it
  was an implementation artifact, not geometry — the frontier result is now trustworthy.**
- **01–03 demos 1.0.0** — initial stable reproductions of the foundational results.
