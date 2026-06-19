# CLAUDE.md

> **Project-wide working rules and cross-repo context live in the FCM umbrella repo's `CLAUDE.md`**,
> loaded automatically when you work from the umbrella root. If you opened this repo directly instead
> of via the umbrella, relaunch from the umbrella root for the full context. This file holds only this
> repo's specific instructions.

Instructions for Claude (and other LLM agents) working in this repository.

## What this project is

`evennia-targeting` is a library that adds composable targeting predicates and content-filtering helpers to [Evennia](https://www.evennia.com/). Predicates are pure `(obj, caller) -> bool` functions; helpers walk `room.contents` (or any container's contents) once, apply a predicate stack, and delegate string matching to Evennia's native `caller.search()`. The library expresses filters Evennia's native search kwargs cannot — runtime state (hp, height, combat side), caller identity, typeclass EXCLUSION (not inclusion), and runtime lock checks. Tagline: **"Composable targeting predicates and content-filtering helpers for Evennia — layered on top of `caller.search()` rather than replacing it."**

The library is Evennia-flavored and primarily intended for use on FullCircleMUD, but is FCM-agnostic by design: nothing in the library knows about FCM-specific typeclasses, mixins, condition enums, or game systems.

For the big-picture overview, read [README.md](README.md).
For the design wiki, read [docs/INDEX.md](docs/INDEX.md).

## Project status

For the current state of the project — milestones reached, what's pending — see [docs/progress.md](docs/progress.md), the running log of milestones with links to evidence.

## Where to read first

For any non-trivial task, start by reading in this order:

1. [README.md](README.md) — what the project is, status, quick start.
2. [docs/INDEX.md](docs/INDEX.md) — map of all design docs.
3. [docs/architecture.md](docs/architecture.md) — high-level mapping of the targeting surface and the library / consumer ownership boundary. Read this before adding to the library's surface area; it captures decisions already pinned and flags the open questions explicitly.
## Load-bearing architectural principles

These are the principles every implementation decision must respect. Getting them wrong is expensive to undo.

1. **The library does not own game concepts.** Stealth mechanics, height systems, combat sides, group membership, container semantics, lock state — all belong to the consumer game. The library provides infrastructure: the `(obj, caller) -> bool` predicate convention, single-pass `walk_contents` / `bucket_contents` helpers, and a small set of generic predicates that express filters Evennia cannot. When tempted to add a game concept, ask whether it's actually game-specific and should stay in the consumer.
2. **No FCM-specific assumptions.** This library was created in service of FullCircleMUD (FCM). Anything FCM-specific creeping into the library is a code smell. `FCMCharacter`, FCM's `Condition` enum, FCM's `HiddenObjectMixin` / `HeightAwareMixin` / `ContainerMixin`, `combat_side`, `combat_handler`, `get_group_leader`, `is_pet` — all stay in FCM. Default to "consumer concern" when uncertain. The library may ship predicates that *duck-type* against attributes (e.g. `getattr(obj, "is_container", False)`); it must not import consumer typeclasses or enums.
3. **Layer on top of Evennia, do not replace it.** The library complements `caller.search()`; it does not wrap or shadow it. Helpers pre-filter candidates and pass them via the `candidates=` kwarg; string matching, lock checks (`use_locks`), nick substitution (`use_nicks`), multimatch disambiguation, dbref lookups, and the `me`/`self`/`here` shortcuts remain Evennia's job. Any helper that re-implements an Evennia feature is suspect.
4. **Predicates and helpers are added only when a real consumer needs them.** No speculative additions. Each predicate / helper must point at a current caller that requires it. This is the discipline that keeps the surface lean over time — see the same rule in FCM's `utils/targeting/` (the in-game ancestor of this library).
5. **Predicates are pure.** A predicate is `(obj, caller) -> bool` with no side effects, no logging, no message dispatch. Factories that return predicates (e.g. `p_passes_lock(lock_type)`) capture parameters at construction time; the returned predicate is still pure. Helpers that need to emit caller-facing messages do so themselves, not via predicates.
6. **Synthetic content first.** Build the library against synthetic test fixtures the library owns (fake actor / item / room typeclasses, synthetic mixin attributes). Real consumer content surfaces edge cases synthetic fixtures didn't reach; when it does, pause integration, capture the case as a new synthetic fixture, fix against it, resume. Fixtures stay forever as regression coverage.

## Out of scope

Scope boundaries are decided as concrete questions arise, by applying the principles above. The library's surface area will be drawn deliberately as actual design needs surface, with each scope decision captured in docs/ when it is made.

Areas where scope questions are likely to need explicit decisions (TBD when they arrive):

- Whether the library ships any `aoe_*` helpers (FCM has `_resolve_aoe_secondaries` covering safe / unsafe / unsafe_self / unsafe_all_heights / allies), or whether AoE composition is left to the consumer.
- Whether spell-target-type dispatch (FCM's `resolve_target(target_type=...)`) lives in this library at all, or whether the library stops at the primitive layer (predicates + walk/bucket) and consumers compose dispatchers in their own code.
- Whether the library ships any "stock" generic predicates (e.g. `p_living`, `p_not_exit`, `p_passes_lock`) versus leaving every predicate to the consumer.
- Whether to support visibility / stealth predicates via a stable duck-typed contract (e.g. `is_hidden_visible_to(caller)` / `is_height_visible_to(caller)` methods), and what that contract looks like.
- Whether priority-bucketed combat / friendly resolvers (the in/out-of-combat attack/friendly resolvers in FCM's `helpers.py`) belong here or stay consumer-side.

## Working conventions

- **Editing design docs.** Update or add design documents whenever an architectural decision is made or refined. Capture the *why*, not just the *what*. Index new docs in [docs/INDEX.md](docs/INDEX.md).
- **Don't put implementation detail in this file or README.** Link out to docs/ instead. Keep CLAUDE.md and README.md stable; let docs/ churn.
- **License.** BSD 3-Clause. New source files should carry a short SPDX header (`# SPDX-License-Identifier: BSD-3-Clause`) once code starts landing.

## Documentation discipline (load-bearing)

Design documents in `docs/` must reflect decisions **actually discussed and agreed on with the project owner**. They are not a place to forward-design the system from first principles or extrapolate "reasonable defaults" from a starting point.

**Rules:**

1. **Only capture what was discussed and agreed.** If the conversation establishes a principle (e.g. "the library never imports consumer typeclasses"), do not extrapolate it into specifics that were not raised (e.g. an exact duck-typed visibility contract, a fixed set of stock predicates, naming conventions for helpers).
2. **Flag open questions explicitly.** Where a topic has been raised but not resolved, write `[TBD — needs discussion: <what is open>]` in the doc. Future sessions then pick the topic up deliberately rather than inheriting unagreed assumptions.
3. **Distinguish archived material from in-conversation decisions.** Material in `docs/archive/` is preserved historical context, not authoritative. Restating archived content in new docs is acceptable when it provides necessary context, but mark it as such rather than presenting it as a decision freshly made or as canonical project intent.
4. **Smaller is better.** A doc that captures three discussed points faithfully is more useful than one that captures three discussed points plus seven invented ones. Resist the urge to fill out sections "for completeness."

If a session catches itself writing content that goes beyond what was discussed, stop and either remove the extrapolation or convert it to a `[TBD]` marker. Documentation that puts unagreed decisions in the project's mouth is worse than documentation that has gaps.

## Repository layout

```
evennia-targeting/
├── CLAUDE.md                  # this file
├── README.md
├── LICENSE                    # BSD 3-Clause
├── pyproject.toml
├── runtests.py                # standalone test runner (no consumer gamedir needed)
├── .gitignore
├── docs/                    # technical wiki (humans + LLMs)
├── src/
│   └── evennia_targeting/     # library code (src layout)
│       ├── __init__.py
│       ├── apps.py
│       ├── predicates.py
│       ├── helpers.py
│       └── tests.py           # unit tests, run via runtests.py
├── tests/                     # standalone test infrastructure
│   ├── __init__.py
│   ├── test_settings.py
│   └── urls.py
└── examples/                  # demo gamedirs for integration testing
```

## Tools and environment

- Python 3.10+ (pinned via `pyproject.toml`).
- Evennia is a runtime dependency (`pip install evennia`).
- **Tests use Django's test runner via `runtests.py`, not pytest.** No consumer gamedir required. Pattern mirrors `evennia-shards` / `evennia-mob-spawner` / `evennia-world-builder`.
- **No YAML, no Reader.** Unlike `evennia-mob-spawner` and `evennia-world-builder`, this library has no declarative content surface — predicates and helpers are pure Python composed by the consumer.
- **One venv, gitignored.** `evennia-targeting/venv/` holds Evennia + `evennia-targeting` (editable). The library has no other runtime dependencies; the venv stays minimal.

## Sibling libraries to reference

When in doubt about a convention not covered here, look at how a sibling library does it:

- **[../evennia-shards/](../evennia-shards/)** — split-deployment / sharding library; working MVP. Reference for the test-runner pattern, src layout, pyproject.toml shape.
- **[../evennia-world-builder/](../evennia-world-builder/)** — declarative YAML world authoring; partly implemented. Reference for the auto-install `evennia._init` wrap pattern (if this library ever needs admin commands).
- **[../evennia-mob-spawner/](../evennia-mob-spawner/)** — declarative YAML mob spawning; working MVP. Reference for the LoadedRule / predicate-tier pattern (if this library ever grows a tiered validator).