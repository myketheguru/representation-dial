# Study ladder — getting to (and past) everything in the search/representation arc

Organized beginner → advanced in tiers. Each tier lists topics with *why it mattered in this
conversation* and one canonical resource. You don't need all of it to depth — the **critical
path** (marked ★) is what the core argument rests on; the rest deepens or branches by lane
(Geometry/Representation = lane A, Hardware = lane B). Resources are canonical; substitute freely.

---

## Tier 0 — Foundations (prerequisites; skim what you know)
- ★ **Discrete math & proof** — sets, logic, combinatorics, induction. *Everything downstream is
  stated as theorems.* — *Book of Proof* (Hammack, free).
- ★ **Probability & statistics** — distributions, expectation, conditional prob, Bayes. *Base rates,
  lift, mutual information, NFL all live here.* — *Introduction to Probability* (Blitzstein & Hwang).
- ★ **Linear algebra** — vectors, matrices, eigen/SVD, inner products, norms. *Embeddings, Fourier,
  PCA, the whole geometry lane.* — Strang, *Linear Algebra and Its Applications* (or his MIT OCW).
- ★ **Algorithms & data structures** — big-O, graphs, search, recursion, dynamic programming.
  *Search, DP, treewidth, backward induction.* — CLRS, *Introduction to Algorithms* (reference).
- **Programming for experiments** — Python, numpy, plotting. *Every test we ran.* — any solid
  numpy/matplotlib tutorial.

## Tier 1 — Information & computation (the spine) ★
- ★ **Information theory** — entropy, mutual information, coding, channel/Shannon limits. *MI as the
  discrimination objective; Shannon counting = the incompressibility floor.* — Cover & Thomas,
  *Elements of Information Theory* (or MacKay, *ITILA*, free).
- ★ **Computability** — Turing machines, decidability, the halting problem. *"Arbitrary search"
  includes the undecidable.* — Sipser, *Introduction to the Theory of Computation* (Part 1).
- ★ **Complexity theory** — P, NP, PSPACE, EXPTIME, reductions, completeness, the **time hierarchy
  theorem**. *Why no universal search-abolisher exists; P≠EXPTIME is proven.* — Sipser (Part 3) →
  Arora & Barak, *Computational Complexity* (advanced).
- ★ **Algorithmic information theory** — Kolmogorov complexity, the **invariance theorem**, MDL,
  Solomonoff induction, the **structure function / sophistication**, logical depth. *The exact
  structure-vs-residual split; representation-independence up to O(1).* — Li & Vitányi, *An
  Introduction to Kolmogorov Complexity and Its Applications*.

## Tier 2 — Structure & search (the conservation core) ★
- ★ **SAT / CSP** — DPLL, resolution, **Schaefer's dichotomy**, XOR-SAT/Gaussian, Horn, 2-SAT.
  *Structured-NP collapse, the knife-edge, Tseitin.* — Biere et al., *Handbook of Satisfiability*
  (skim) + the Schaefer'78 dichotomy paper.
- ★ **Graphical models & treewidth** — variable elimination, junction trees, **valuation/information
  algebras**, treewidth as the cost invariant. *The conservation experiment.* — Koller & Friedman,
  *Probabilistic Graphical Models* (the local-computation chapters).
- **Proof complexity** — resolution lower bounds, why Tseitin/parity is exponential for DPLL but
  trivial for Gaussian. *Matched-prior-required, proven.* — survey: Nordström, *Proof complexity*.
- **Optimization** — convex optimization, **duality**, dynamic programming. *Structured collapse via
  convexity / optimal substructure.* — Boyd & Vandenberghe, *Convex Optimization* (free).

## Tier 3 — Learning theory & inductive bias ★
- ★ **PAC learning & VC dimension** — sample complexity, capacity, the **No-Free-Lunch theorems**.
  *"Capability tracks the prior," made formal.* — Shalev-Shwartz & Ben-David, *Understanding Machine
  Learning* (free).
- ★ **Meta-learning / learning the bias** — when the prior/representation is itself learnable, and
  its limit (only relative to a task-environment). — Baxter, *A Model of Inductive Bias Learning*,
  JAIR 2000.
- **Cryptographic hardness of learning** — one-way functions, why low-DOF can be inaccessible.
  *low-DOF necessary-not-sufficient.* — Katz & Lindell, *Introduction to Modern Cryptography* (Ch.
  on OWFs) + Kearns–Valiant'94.

## Tier 4 — Geometry, symmetry, representation (LANE A — the access frontier) ★
- ★ **Fourier analysis & the FFT** — convolution, the DFT, why FFT is fast. *Representation aligned
  with cyclic symmetry diagonalizes convolution.* — Brigham, *The Fast Fourier Transform*; or 3Blue1Brown.
- ★ **Group theory & representation theory; harmonic analysis** — irreducible representations,
  Schur's lemma, generalized Fourier on groups. *The general "structure-revealing basis = the
  symmetry's irreps."* — Artin, *Algebra* (groups) → Diaconis, *Group Representations in Probability
  and Statistics* (free).
- ★ **Differential & Riemannian geometry; hyperbolic geometry** — manifolds, curvature, geodesics,
  the Poincaré ball. *Non-Euclidean access; the access/search-split study.* — do Carmo (rigorous) or
  Needham, *Visual Differential Geometry* (intuitive).
- ★ **Geometric deep learning** — symmetry/equivariance as the right inductive bias; the Erlangen
  view. *The same thread as our group-theory toy.* — Bronstein, Bruna, Cohen, Veličković,
  *Geometric Deep Learning* (proto-book, free).
- ★ **Embeddings & vector search** — word/sentence embeddings, cosine similarity, ANN/**HNSW**,
  **Poincaré/hyperbolic embeddings**. *Retrieval-search; the access study tooling.* — Nickel & Kiela,
  *Poincaré Embeddings* (2017) + the FAISS / HNSW docs.
- **Topological data analysis** — persistent homology, the shape of data. *The TDA framing Gemini
  invoked.* — Edelsbrunner & Harer, *Computational Topology*; or Ghrist, *Elementary Applied Topology*.

## Tier 5 — Causality ★
- ★ **Causal inference foundations** — SCMs, **Pearl's hierarchy** (association/intervention/
  counterfactual), the **Causal Hierarchy Theorem**, Markov equivalence, identifiability (LiNGAM/
  ANM), causal discovery (PC/GES). *Compression is causally blind; intervention is irreducible.* —
  Pearl, *The Book of Why* (gentle) → Peters, Janzing & Schölkopf, *Elements of Causal Inference* (free).

## Tier 6 — Research frontier (where the open questions are)
- **Computational–statistical gaps** — SQ / low-degree / SoS / OGP lower bounds, planted clique.
  *Low-DOF-but-hard; no average-case gap known NP-hard.* — Wein survey, arXiv:2506.10748.
- **Library learning / program synthesis** — DreamCoder, Stitch, LILO; MDL-driven abstraction
  invention. *Compression finds frequent, not discriminative, structure.* — DreamCoder (Ellis et
  al. 2021) + Stitch (POPL 2023).
- **Open-endedness & discovery** — novelty search, quality-diversity (MAP-Elites), PowerPlay;
  FunSearch/AlphaEvolve. *Inventing new primitives vs composing old ones.* — Lehman & Stanley
  (novelty search) + Hughes et al., *Open-Endedness Essential for ASI* (ICML 2024).
- **Physics of learnability** — why the world has a small reusable structural vocabulary. — Lin,
  Tegmark & Rolnick, *Why does deep and cheap learning work so well?* (2017).

## Tier 7 — Hardware / substrate (LANE B — pursue only if it calls you)
- ★ **Computer architecture** — the **Von Neumann bottleneck**, memory hierarchy, data-movement
  cost. *Neuromorphic cuts energy/latency, not search.* — Patterson & Hennessy, *Computer
  Organization and Design*.
- ★ **Digital design & HDL** — logic, Verilog/VHDL, FPGAs. *Build a small accelerator at home.* —
  Harris & Harris, *Digital Design and Computer Architecture* (+ an FPGA board).
- ★ **Neuromorphic computing & SNNs** — spiking nets, event-driven compute, processing-in-memory.
  — `snnTorch` tutorials (gentle) → Intel **Lava** framework; apply to the Intel Neuromorphic
  Research Community (INRC) for Loihi 2 access.
- **Sparsity & quantization / hardware-algorithm co-design** — shrinking models onto memory arrays.
  — recent survey papers + the snnTorch/Lava docs.

---

## How to use this ladder (don't boil the ocean)
- The **critical path** for the *argument* is Tiers 1–3 + the relevant half of Tier 4. That's what
  makes the whole conversation rigorous rather than vibes.
- Pick a **lane**: A (geometry/representation, Tier 4 deep) properly supports the access/search
  study; B (hardware, Tier 7) is a multi-year build with its own prerequisites.
- **Learn by shipping:** pair each tier with a tiny experiment (you already do this). Reading Tier 4
  while building `STUDY_access_search_split.md` is worth more than reading it cover-to-cover first.
- Realistic ordering if entering the geometry lane: Tier 0 gaps → Tier 1 (info+complexity) → Tier 3
  (NFL/PAC) → Tier 4 (Fourier→groups→Riemannian→GDL→embeddings) → build the study → Tier 5/6 as you go.
