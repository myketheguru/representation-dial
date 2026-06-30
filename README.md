# The powers and limits of representation

*Can a better representation abolish search? Where does it help, where can't it, and why?*
A progressive tour of small, runnable, exact-ground-truth experiments — reproducing established
results from scratch and pushing to a live frontier. **Every claim here is a script you can run.**

> Engineering discipline pointed at foundational science: every claim is a small, runnable,
> falsifiable experiment — and the code prints its own verdict.

If you read one thing, read **[POSITION_NOTE.md](POSITION_NOTE.md)** — the perspective that ties it
all together (and is honest about what's rediscovery, what's original, and what failed). For how this
repo fits the larger program (three tracks), see **[PROJECTS.md](PROJECTS.md)**.

> **Part of one body of curious work.** This repo is Tracks **A** (foundations) and **C** (the
> frontier). Its companion — Track **B**, the original concept-rediscovery experiment — lives at
> **[github.com/myketheguru/concept-rediscovery](https://github.com/myketheguru/concept-rediscovery)**.

## The tour (follow in order)
Each folder has its own README, the artifacts, and *what each one tests*.

1. **[01_the_limit/](01_the_limit/)** — *Search is conserved.* No universal algebra makes arbitrary
   search direct; the cost floor (treewidth) is representation-invariant, and incompressibility is
   representation-independent.
2. **[02_the_power/](02_the_power/)** — *...but structured search collapses, under the matched prior.*
   The same parity problem is instant for Gaussian and exponential for DPLL; a representation works by
   aligning with the data's structure (FFT = a group's irreducible representations).
3. **[03_the_boundary/](03_the_boundary/)** — *Where the power stops.* Low degrees-of-freedom is
   necessary but not sufficient (structure can be cryptographically hidden); compression is causally
   blind (it can't reach intervention).
4. **[04_the_frontier/](04_the_frontier/)** — *Representation as the access/search dial.* The active
   experiment: does matching the geometry to the structure convert search into cheap access — and how
   far does it go? (In progress; honest, partial results.)

The arc: **you can't abolish search, but the representation sets how much of a problem is cheap
access vs irreducible search — and the wins live exactly at the structure, never beyond it.**

## Running the demos
Pure Python; only `04_the_frontier/` needs numpy (`pip install numpy`). Each script prints its own
verdict. Run from inside its folder, e.g.:
```
cd 01_the_limit && python treewidth_conservation.py
cd 04_the_frontier && python access_search_split.py        # v1: structure sweep
cd 04_the_frontier && python access_search_split_v2.py      # v2: dimension sweep
```
Artifact versions are tracked in **[VERSIONS.md](VERSIONS.md)**.

## About
By **Micheal Ezeoda** (`myketheguru` on GitHub, `_darkmyke` on socials) — a software engineer (10+ years) with broad scientific curiosity, doing independent
foundational research on representation. Background reading map: **[CURRICULUM.md](CURRICULUM.md)**.

## Honest framing (the standard)
The **foundations** (folders 01–03) *reproduce established results* — treewidth conservation
(Kohlas), Schaefer's dichotomy, Kolmogorov invariance, Pearl's causal hierarchy, No-Free-Lunch
(Wolpert–Macready). Credited, not claimed. The **frontier** (folder 04) and the related concept-
rediscovery work are where the original experiments — and the honest null results — live. Nothing
here claims a new theorem; the contribution is a clear, falsifiable, ground-truth-honest map.
