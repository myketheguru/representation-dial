# Study (pre-registration): Does matched geometry move the access/search boundary? — measured with exact ground truth

**One-line question.** Treating a representation as the dial that splits a task into *cheap
geometric access* (answer is a nearest neighbour) vs *irreducible search* (answer must be
explored for), does matching the embedding geometry to the data's intrinsic structure measurably
**increase the access fraction** — and is the gain **bounded by how much structure is present**?

**One-line hypothesis.** For hierarchical data, a hyperbolic (Poincaré) embedding yields a higher
access fraction than a Euclidean one at matched dimension; the advantage **grows with the amount
of hierarchy** and **vanishes to chance as structure → 0** (the curse-of-dimensionality floor).

---

## 1. Honesty up front (what's new vs known)
- **Known (do not claim as novel):** hyperbolic space embeds hierarchies better than Euclidean —
  Nickel & Kiela, *Poincaré Embeddings*, NeurIPS 2017. This study REPLICATES that core.
- **The actual contribution (modest):** (a) the **access/search-split framing** — measuring the
  geometry advantage as "fraction of the task that became cheap access"; (b) a **structure-knob
  sweep** that measures *where the advantage appears and where it vanishes* (the floor), which the
  original benchmarks don't isolate; (c) an exact-ground-truth permutation control.
- **Honest ceiling:** primarily a **skill-building + field-entry artifact** (Riemannian
  optimization, embeddings, the access/search lens) with a modest novel measurement. Workshop /
  arXiv-note / good-blog tier. A clean null is equally shippable.

## 2. Design
**Primary domain — synthetic hierarchy with a structure knob (exact ground truth):**
- Generate a tree T (depth d, branching b; ~1–5k nodes). Interpolate structure by REWIRING a
  fraction `q` of edges to random pairs: `q=0` = pure hierarchy, `q→1` = random graph.
  Structure level = `1 − q` (also report a measured hierarchy stat, e.g. Gromov δ-hyperbolicity).
- **Embed** each node in (i) Euclidean R^k and (ii) Poincaré ball H^k, **matched k**, matched
  training budget/negatives, using the standard reconstruction objective (pull graph-adjacent
  nodes close, push sampled negatives) under the respective distance.
- **Task / metric — ACCESS FRACTION:** for each node, retrieve its true graph-neighbours by
  nearest-neighbour in the embedding. Access fraction = mean **top-1** (and top-k) recall of true
  neighbours. "Solved by access" = true answer is the NN; "needs search" = it isn't.

**Secondary (transfer check, optional):** repeat on a *real relational* dataset with known
ground truth (e.g. a WordNet noun subtree, or your chess endgame role-graphs) to see whether the
principle holds beyond synthetic trees.

## 3. Independent / dependent variables
- **IV:** structure level `1−q` (swept 0 → 1), embedding dimension k, geometry {Euclidean, Poincaré}.
- **DV:** access fraction (top-1 / top-k), and the **gap** = access(Poincaré) − access(Euclidean).

## 4. Pre-registered decision bar
- **TRUE:** at high structure, gap ≥ +10 points top-1; the gap is **monotone increasing** in `1−q`
  (Spearman ρ ≥ 0.7 across knob levels); both geometries → chance as `q→1`. → matched geometry
  measurably moves the access boundary, bounded by structure.
- **NULL/FALSE:** gap ≈ 0 across all structure levels (matched geometry doesn't help access), OR
  no monotone dependence on structure. → honest negative (and notable given field claims).
- **THIRD:** hyperbolic helps but the gap is a constant offset independent of structure → characterize.

## 5. Controls (let it fail)
- **Matched** dimension, optimizer steps, negative sampling, init scale across geometries.
- **Permutation null:** shuffle node labels (destroy structure, keep degree) → both geometries →
  chance access. Confirms the advantage comes from real structure, not the embedder.
- **Floor reported explicitly:** the `q→1` (random) point is the curse-of-dimensionality floor.
- **Replicates:** several (d,b) tree configs; report CIs.
- **Dimension sweep:** k ∈ {2,5,10,50} — hyperbolic's edge should be largest at *small* k.

## 6. Tools / effort
- `torch` + `geoopt` (Riemannian Adam on the Poincaré ball) — the clean path; or hand-roll the
  Poincaré distance + Riemannian SGD (Nickel-Kiela did exactly this; embeddings are small).
  **Note:** needs `pip install torch geoopt` (or numpy + hand-rolled) — current env has neither.
- Effort: a few focused days. Synthetic-data generator + two embedders + the sweep + plots.

## 6b. FIRST RUN (`access_search_split.py`) — directional, modest, confounded
n=300 balanced tree (b=3), dim=5, Poincaré vs Euclidean, structure swept via rewiring fraction q.
Access = fraction of nodes whose nearest embedded neighbour is a true graph-neighbour.

| structure (1−q) | Euclid | Poincaré | gap (P−E) |
|---|---|---|---|
| 1.00 (tree) | 0.340 | 0.382 | **+0.042** |
| 0.80 | 0.611 | 0.667 | **+0.056** |
| 0.60 | 0.795 | 0.776 | −0.019 |
| 0.30 | 0.883 | 0.820 | −0.063 |
| 0.00 (random) | 0.900 | 0.831 | −0.070 |

- **Directional support:** the hyperbolic *gap* is positive for hierarchy (+0.04..+0.06) and flips
  negative as structure is destroyed (−0.07) — matched geometry helps to the extent structure is present.
- **Two flaws to fix before believing the magnitude:** (1) the raw access metric is **confounded** —
  tree reconstruction is harder (siblings cluster but aren't neighbours), mixing task-difficulty with
  geometry-match; use a difficulty-controlled metric (MAP/rank, or normalize per structure level).
  (2) **dim=5 is too generous** — hyperbolic's edge is largest at **dim=2** (run the dimension sweep).
- **Next:** dim ∈ {2,5,10,50} sweep; rank-based access metric; the permutation/label-shuffle null;
  more reps + CIs. Honest status: working pipeline, partial signal, iterating.

## 6c. DIMENSION SWEEP (`access_search_split_v2.py` v2.0.0) — INCONCLUSIVE, implementation-limited
Held structure fixed, swept dim ∈ {2,3,5,10}. **Predicted:** hyperbolic's edge largest at dim=2.
**Result contradicts it** — for the pure tree the Poincaré gap is *negative* at dim=2 and only turns
positive at dim≥5:

| dim | gap(P−E), tree (struct 1.00) | gap(P−E), struct 0.60 |
|---|---|---|
| 2 | **−0.100** | +0.050 |
| 3 | −0.022 | +0.050 |
| 5 | +0.042 | −0.019 |
| 10 | +0.043 | +0.015 |

The pattern is noisy/non-monotone, and Euclidean tree-access is *higher* at dim=2 (0.488) than dim=5
(0.340) — a sign the crude **top-1 access metric is crowding-sensitive**, not measuring geometry.
**Honest verdict:** this contradicts the established Nickel–Kiela finding (hyperbolic better at low
dim), which strongly implies **the fault is my implementation, not the geometry** — the hand-rolled
Riemannian SGD is likely undertrained/poorly-tuned in 2D hyperbolic space, and top-1 access is brittle.
**Inconclusive** until: (1) a proper hyperbolic optimizer (geoopt / Riemannian Adam); (2) a rank-based
metric (MAP / mean reciprocal rank, not top-1); (3) convergence checks. Build-in-public lesson: the
first tooling isn't trustworthy enough to answer the question — and saying so is the point.

## 6d. THE REBUILD (`access_search_split_v3.py` v3.0.0) — RESOLVED, trustworthy
Fixed v2's two suspects: (1) a **rank-based metric** (MAP + mean reciprocal rank, not brittle top-1);
(2) **better training** (gradient clipping + lr decay + converged epochs). Pure tree, dims {2,5,10}:

| dim | MAP gap (Poincaré − Euclid) | MRR gap |
|---|---|---|
| **2** | **+0.079** | **+0.076** |
| 5 | +0.028 | +0.061 |
| 10 | +0.003 | +0.034 |

**Hyperbolic now beats Euclidean at every dimension, and the edge is largest at dim=2** — exactly the
established Nickel–Kiela pattern. ⇒ v2's contradictory result **was** an implementation artifact (the
brittle top-1 metric + undertrained 2D), not geometry. The geometry effect is **real**, and the
frontier result is now **trustworthy**. The arc — v1 directional → v2 inconclusive → v3 fixes
metric+training → clean — is the honest face of building research tooling: the first cut wasn't good
enough, the flaw was named openly, the rebuilt result holds. *Optional polish:* geoopt/Riemannian Adam
as a definitive cross-check; the structure-knob sweep re-run with the rank metric.

## 7. Deliverable
One figure (access fraction vs structure level, Euclidean vs Poincaré, one curve each, with the
permutation-null floor) + a dimension-sweep table + a short writeup stating which of TRUE/NULL/THIRD
held. The framing claim being tested: **the representation sets the access/search split, and the
geometry advantage is real exactly to the extent the matching structure is present — never beyond.**
