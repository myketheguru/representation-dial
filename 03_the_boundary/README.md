# 03 · The boundary — where the power stops

**Question:** if matched structure can collapse search, what limits it?
**Answer:** two hard boundaries — structure can be *present but inaccessible*, and compression can
*describe but not explain*.

| artifact (version) | what it tests | the result |
|---|---|---|
| `hidden_structure.py` (1.0.0) | Can a standard structure-exploiter (gzip) find low degrees-of-freedom that are cryptographically hidden? | A string expanded from a 32-bit seed via a hash is gzip-incompressible (ratio 1.001), **indistinguishable from true random** — its 32 bits of structure are hidden. Low-DOF is *necessary but not sufficient*; the constraint must be computationally accessible. The gap is cryptography / one-way functions. |
| `causal_compression.py` (1.0.0) | Do two opposite causal models fit the same observations equally, yet predict interventions differently? | X→Y and Y→X fit identically (log-likelihood −14162.2 = −14162.2) but predict E[Y \| do(X=3)] = 6 vs 0. Compression *selects* explanations; it cannot *reach* causation (Pearl's hierarchy) — that needs intervention. |

**Run:** `python hidden_structure.py` · `python causal_compression.py` (pure Python).

**Takeaway:** a representation's power is bounded twice over — by *accessibility* (structure you can't
efficiently find) and by *causality* (what passive data can't tell you). *Established — one-way
functions, Pearl's causal hierarchy theorem — reproduced here.*
