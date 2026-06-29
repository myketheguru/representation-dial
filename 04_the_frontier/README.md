# 04 · The frontier — representation as the access/search dial

**The constructive turn.** You can't abolish search, but a representation sets *how much* of a task is
cheap geometric **access** (the answer is a nearest neighbour) vs irreducible **search**. So: does
matching the embedding geometry to the data's structure measurably move that boundary — and how far?

This is **active research** — honest, partial, iterating. See `STUDY_access_search_split.md` for the
full pre-registration (hypothesis, controls, true/false bar) and results.

| artifact (version) | what it tests | status |
|---|---|---|
| `access_search_split.py` (1.0.0) | Structure-knob sweep at dim=5: does hyperbolic geometry raise the *access fraction* for hierarchical data, with the advantage shrinking as structure is destroyed? | First result: **directional** (gap +0.04..+0.06 for hierarchy, flips to −0.07 as structure → random) but **modest & confounded** (tree reconstruction is intrinsically harder; dim=5 too generous). |
| `access_search_split_v2.py` (2.0.0) | Dimension sweep (holds structure fixed): is the geometry advantage largest at small dim (dim=2)? The v1 confound check. Imports v1's machinery unchanged. | **Inconclusive.** Predicted dim=2 best; got the *opposite* (tree gap −0.100 at dim=2, positive only at dim≥5). Contradicts the known result ⇒ likely an **implementation** fault (undertrained 2D optimizer + brittle top-1 metric), not geometry. Needs a real hyperbolic optimizer + rank metric. |

**Run** (from inside this folder, needs numpy): `python access_search_split.py` · `python access_search_split_v2.py`.

**Takeaway (so far):** v1 shows a *directional* effect (geometry helps exactly where structure is), but
v2 (the dimension sweep) contradicted its own prediction — and that contradiction most likely indicts
**my implementation, not the geometry** (a hand-rolled 2D Riemannian optimizer + a brittle top-1 metric).
Honest status: **the current tooling isn't trustworthy enough to answer the question.** Next: a proper
hyperbolic optimizer (geoopt / Riemannian Adam) + a rank-based metric, then re-run. The known core
(Nickel & Kiela, 2017) says hyperbolic *should* win for hierarchy; the **access/search-split framing +
structure-knob + floor** is the contribution. Build-in-public means showing when your own tooling falls
short — not hiding it.
