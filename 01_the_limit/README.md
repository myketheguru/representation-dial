# 01 · The limit — search is conserved

**Question:** can a representation make *arbitrary* search direct (no exploration)?
**Answer:** no. The work is conserved; a representation can relocate it but never destroy it — and
the cost floor is a structural invariant no representation beats.

| artifact (version) | what it tests | the result |
|---|---|---|
| `treewidth_conservation.py` (1.0.0) | Does any elimination order (= representation) beat the treewidth cost floor? Does relabeling the graph change it? | Many orders span a wide cost range, but none beats the floor; relabeling leaves it **exactly** unchanged (10,10,10,10,10). The conserved quantity is structural. |
| `incompressibility.py` (1.0.0) | Is a *random* Boolean function small in any representation (DNF / ANF / BDD)? Is a *structured* one small in its matched basis? | Parity is tiny in ANF (12) and huge in DNF (2048); a random function is large in **all three**. The floor is representation-independent (Kolmogorov invariance). |

**Run:** `python treewidth_conservation.py` · `python incompressibility.py` (pure Python).

**Takeaway:** no universal solvent for search. What's conserved is the problem's structural/search
content; representation moves it around (into precomputation, size, or an assumed prior) but the floor
holds. *Established results — Kohlas (valuation algebras), Kolmogorov invariance — reproduced here.*
