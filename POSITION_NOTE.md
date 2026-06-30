# Representation as the access/search dial: powers, limits, and honest ceilings

*A perspective note. Position: this organizes established results (credited), reproduces them as
small runnable demos, and reports a few original experiments — including null results. It claims
no new theorems; its contribution is a clear, falsifiable, ground-truth-honest map.*

**Author:** darkmyke — software engineer (10+ yrs), independent researcher.
**Artifacts:** every claim below has a runnable demo in this repo (named + versioned). Run them.

---

## TL;DR
"Can a better representation abolish search?" splits into two questions with opposite answers.
For **arbitrary** problems, **no** — the search content of a problem is conserved; representation
relocates it (into precomputation, representation size, or an assumed prior) but never destroys it.
For **structured** problems, a representation matched to the structure can collapse search into
**direct geometric access** — but only to the extent the structure is actually there, and only with
the *matched* prior. The practical upshot: **a representation is a dial that sets how much of a task
is cheap access vs irreducible search; engineering that dial is the whole game, and it is bounded by
the structure present.** Two real frontiers follow — *representational geometry* (find the manifold
matched to the structure) and *substrate* (cheapen execution of the irreducible remainder) — and
both are relocations, not abolitions.

## 1. The limit: search is conserved
- **No universal solvent.** A transform that made *arbitrary* search direct would collapse proven
  complexity separations: generalized chess/Go are EXPTIME-complete and P ≠ EXPTIME is a *theorem*
  (time hierarchy). It would also have to solve undecidable problems. So the general claim is dead
  on arrival.
- **The conserved quantity is structural.** The literal "information algebra" that turns inference
  search into direct local computation exists — valuation algebras / variable elimination (Kohlas;
  Shenoy–Shafer) — and its cost is exactly **2^treewidth**, a representation-*invariant* floor.
  *Demo:* `treewidth_conservation` — different elimination orders (representations) span a wide cost
  range, but none beats the treewidth floor, and relabeling the graph leaves it exactly unchanged.
- **The floor is representation-independent.** By the Kolmogorov invariance theorem, incompressibility
  is machine-independent up to an additive constant: almost all objects are large in *every*
  representation. *Demo:* `incompressibility` — parity is tiny in the matched basis (ANF) and huge in
  the wrong one (DNF), while a *random* function is large in DNF, ANF, and BDD alike.

## 2. The power: structured search collapses — under the matched prior
- **Structured subclasses do collapse to direct, polynomial computation** — but each via a *specific*
  algebra matched to its structure, on a proven knife-edge (Schaefer's dichotomy for Boolean CSP).
  *Demo:* `structured_np` — XOR-SAT (linear) is solved instantly by Gaussian elimination; the *same*
  parity problem (a Tseitin formula) is *provably exponential* for general DPLL search. Same problem,
  matched prior = instant, mismatched = exponential. 2-SAT collapses via a different matched algebra
  (implication-graph SCC); 3-SAT, with no matched algebra, stays hard.
- **A representation works by aligning with the data's structure.** *Demo:* `fourier_alignment` — the
  FFT basis (the irreducible representations of the cyclic group) sends a convolution operator to
  off-diagonal energy 0.0000 (perfectly diagonal) and does nothing (0.97) for a structureless
  operator. FFT, Gaussian elimination, dynamic programming, hashing — each aligns the free operations
  with a different invariant. This is the geometric-deep-learning thesis (Bronstein et al., 2021) in
  miniature.

## 3. The boundary: where the power stops
- **Low effective degrees-of-freedom is necessary but NOT sufficient.** Structure can be real and yet
  computationally inaccessible. *Demo:* `hidden_structure` — a string expanded from a 32-bit seed
  through a hash is gzip-incompressible, indistinguishable from true randomness; its 32 bits of true
  structure are *hidden*. The gap between "low-DOF" and "exploitable low-DOF" is exactly cryptography /
  one-way functions, and (via hardness-of-learning) bounds what is discoverable.
- **Compression cannot reach causation.** *Demo:* `causal_compression` — two structural models, X→Y
  and Y→X, fit the same observational data identically (log-likelihood −14162.2 = −14162.2) yet give
  opposite interventional predictions (E[Y | do(X=3)] = 6 vs 0). By Pearl's causal hierarchy theorem
  (Bareinboim, Correa, Ibeling, Icard, 2022), observation cannot reach intervention; compression
  *selects* explanations but does not *generate* causal ones — that needs intervention.

## 4. The synthesis: the dial, and what sets it
A representation does not change a problem's total work; it sets **how much is cheap access and how
much is irreducible search** — by encoding the structured part as geometry (proximity = answer) and
leaving the structure-free residual to exploration. The slogan "capability tracks the prior" is best
stated, after Wolpert–Macready's No-Free-Lunch, as **capability tracks the alignment between the prior
and the world's structure.** The prior is not magic; it works because reality has exploitable
regularities (symmetry, locality, hierarchy — Lin, Tegmark & Rolnick, 2017). The wins are real, and
they live exactly at the structure, never beyond it.

## 5. The frontier (active, with honest ceilings)
- **Representational geometry — measuring the dial.** Does matching the embedding geometry to the
  structure measurably raise the access fraction, bounded by structure? *Artifact:* `access_search_split`
  — first runs show a *directional* signal (hyperbolic helps hierarchy, loses its edge as structure is
  destroyed) but **modest and confounded**; iterating on the metric and dimension. Replicates the known
  core (Nickel & Kiela, 2017); the framing (access/search split + structure-knob + floor) is the angle.
- **The substrate** cheapens *execution* of the irreducible remainder (memory–compute fusion;
  neuromorphic) — energy and latency, not complexity. A different, real win; not an abolition.
- **Honest ceilings, on the record.** In a related ground-truth setting (chess endgames, exact
  tablebase labels), two pre-registered hypotheses of mine **nulled** — a predicted compression-vs-
  discrimination gap was +0.004, then +0.000 on a stricter rerun; the cause was feature redundancy.
  Reporting that is the method, not a footnote.

## 6. What is open (honestly)
No average-case computational–statistical gap is known to be NP-hard (Wein, 2025); a predictive theory
of *which* structures are discoverable vs cryptographically hidden does not exist; and there is no
theory of inventing a genuinely *new* representational primitive (vs composing known ones). These are
theory frontiers; this note does not solve them — it locates them.

## 7. Method (the standard I hold)
Exact ground truth where possible; every claim a falsifiable, runnable demo; established results
credited by name. Engineering discipline pointed at foundational science.

## Selected references (established results organized here)
Wolpert & Macready, *No Free Lunch* (1997) · Schaefer, *Complexity of satisfiability problems* (1978) ·
Kohlas, *Information Algebras* · Li & Vitányi, *Kolmogorov Complexity* · Bareinboim, Correa, Ibeling &
Icard, *On Pearl's Hierarchy* (2022) · Nickel & Kiela, *Poincaré Embeddings* (2017) · Bronstein, Bruna,
Cohen & Veličković, *Geometric Deep Learning* (2021) · Lin, Tegmark & Rolnick, *Why does deep and cheap
learning work* (2017) · Wein, *Computational complexity of statistics* (2025).
