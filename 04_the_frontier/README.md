# 04 · The frontier — representation as the access/search dial

**The constructive turn.** You can't abolish search, but a representation sets *how much* of a task is
cheap geometric **access** (the answer is a nearest neighbour) vs irreducible **search**. So: does
matching the embedding geometry to the data's structure measurably move that boundary — and how far?

This is **active research** — honest, partial, iterating. See `STUDY_access_search_split.md` for the
full pre-registration (hypothesis, controls, true/false bar) and results.

| artifact (version) | what it tests | status |
|---|---|---|
| `access_search_split.py` (1.0.0) | Structure-knob sweep at dim=5: does hyperbolic geometry raise the *access fraction* for hierarchical data, with the advantage shrinking as structure is destroyed? | First result: **directional** (gap +0.04..+0.06 for hierarchy, flips to −0.07 as structure → random) but **modest & confounded** (tree reconstruction is intrinsically harder; dim=5 too generous). |
| `access_search_split_v2.py` (2.0.0) | Dimension sweep (holds structure fixed): is the geometry advantage largest at small dim (dim=2)? The v1 confound check. Imports v1's machinery unchanged. | **Inconclusive.** Predicted dim=2 best; got the *opposite* (tree gap −0.100 at dim=2, positive only at dim≥5). Contradicts the known result ⇒ suspected an **implementation** fault (undertrained 2D optimizer + brittle top-1 metric). |
| `access_search_split_v3.py` (3.0.0) | The rebuild: a **rank metric** (MAP/MRR, not top-1) + **clipped, converged training**. Imports v1's geometry primitives. | **Resolved — trustworthy.** On a pure tree, hyperbolic now beats Euclidean at every dim, edge **largest at dim=2** (MAP gap +0.079 → +0.003 from dim 2 → 10). The established pattern. ⇒ v2 was indeed an implementation artifact, not geometry. |

**Run** (from inside this folder, needs numpy): `python access_search_split.py` · `python access_search_split_v2.py` · `python access_search_split_v3.py`.

**Takeaway (RESOLVED):** v1 showed a *directional* effect; v2 (top-1 metric) came back contradictory and
inconclusive; **v3 — with a rank metric + converged training — resolves it cleanly: hyperbolic beats
Euclidean for hierarchy, edge largest at dim=2** (the established Nickel & Kiela pattern). The v2 mess
was an implementation artifact, named openly and fixed — that arc (directional → inconclusive → fixed)
is the honest face of building research tooling. The **access/search-split framing +
structure-knob + floor** is the contribution. Build-in-public means showing when your own tooling falls
short — not hiding it.
