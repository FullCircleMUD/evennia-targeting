# Architecture

High-level mapping of the targeting surface and the library / consumer boundary for each piece. The doc tracks alongside the implementation — every decision below should be reflected in code, every behaviour in code should be reflected here. If you find a gap, treat it as a bug in this doc.

## Status

**Scaffold.** Repository scaffold is in place; no library code yet. This document captures the **shape the library is being extracted from**, not finalised architectural decisions. Sections marked `[TBD]` are explicit open questions to resolve before code lands.

## Guiding principle

**Layer on top of Evennia, do not replace it.** The library's job is to express filters Evennia's native `search()` cannot — runtime state, caller identity, typeclass EXCLUSION, runtime lock checks — and to compose them via a single-pass walk of `room.contents` (or any container's contents). String matching, the `search` lock, nick substitution, multimatch disambiguation, dbref lookups, and the `me`/`self`/`here` shortcuts all stay Evennia's. The library hands Evennia a pre-filtered candidate list via the `candidates=` kwarg and Evennia does the rest.

This means: **the library never re-implements an Evennia feature.** Any helper that looks like it's shadowing `caller.search` is suspect.

## Extraction substrate

The library generalises the in-game `utils/targeting/` package that lives in the FCM gamedir at `FCM/src/game/utils/targeting/`. That package contains:

- **`predicates.py`** — `(obj, caller) -> bool` predicates. Some are generic and library-shaped (`p_passes_lock(lock_type)`, `p_same_height_value(height)`); many are FCM-coupled (import `FCMCharacter`, FCM's `Condition` enum, `HiddenObjectMixin`-flavoured `is_hidden_visible_to`, `HeightAwareMixin`-flavoured `is_height_visible_to`, `combat_handler` scripts, `combat_side` attributes, `is_container` from FCM's `ContainerMixin`, `get_group_leader` group system, `is_pet` / `owner_key` pet system).
- **`helpers.py`** — `walk_contents` and `bucket_contents` (both generic), plus FCM-coupled resolvers (`resolve_attack_target_in_combat`, `resolve_friendly_target_*`, `resolve_target(target_type=...)` dispatch, `_resolve_aoe_secondaries`).
- **`__init__.py`** — explicit "predicates and helpers are added only when a real consumer requires them" discipline. Exports nothing by default.

The extraction problem is splitting the generic core from the FCM-coupled layers. The library will hold the generic core. FCM keeps the coupled layers — either as a thin shim around library primitives, or as game-side helpers that import from the library.

`[TBD — needs discussion: which specific predicates and helpers move to the library on first cut.]`

## Library surface (intended shape)

The library is expected to expose, at minimum, these primitives — but **each lands only when its first real consumer exists**, per CLAUDE.md principle 4:

- **`walk_contents(caller, source, *predicates) -> list`** — single-pass `source.contents` walk applying every predicate via short-circuit `all()`. Returns the filtered list. The most generic helper; FCM uses it as the universal targeting primitive.
- **`bucket_contents(caller, source, key_fn, *predicates, order=None) -> dict`** — single-pass walk + bucketing. Used for combat side detection, AI threat tiers, multi-faction queries.
- **A small set of stock predicates** with no consumer coupling — exact list `[TBD]`. Strong candidates: `p_passes_lock(lock_type)`, generic exit/typeclass-exclusion predicates.

`[TBD — needs discussion: whether the library ships any duck-typed visibility predicates (e.g. p_visible_to, p_height_visible_to) that read attributes like is_hidden_visible_to / is_height_visible_to off objects without knowing what mixin set them. This works if a stable contract is pinned; otherwise visibility predicates stay consumer-side.]`

`[TBD — needs discussion: whether spell-style target_type dispatch belongs in the library at all. FCM's resolve_target is a large switch over target_type strings ("actor_hostile", "items_inventory", "items_room_all_then_inventory", etc.). The library may stop at primitives and leave dispatch to consumers, or ship a target_type registry that consumers extend.]`

## Library / consumer boundary

| Concern | Lives in | Why |
|---|---|---|
| `(obj, caller) -> bool` convention | Library | The protocol itself is the contract — needs to be stable. |
| Single-pass walk / bucket primitives | Library | Performance-critical loops everyone needs. |
| Generic predicates (lock, typeclass exclusion) | Library | No consumer coupling. |
| FCM `Condition` enum lookups | FCM | Consumer-specific enum; library can't import. |
| FCM mixin attribute reads (`is_container`, `is_locked`) | `[TBD]` | If the library ships duck-typed predicates that read these attributes by name without importing the mixin, they're library-OK. The contract needs to be pinned. |
| Combat side / handler queries | FCM | Combat is a consumer concern; library doesn't know what `combat_side` means. |
| Group membership (`get_group_leader`, `is_pet`) | FCM | Game-system concern. |
| `target_type` dispatch (spell targeting) | `[TBD]` | See above. |
| AoE secondaries (`_resolve_aoe_secondaries`) | `[TBD]` | The shape (safe / unsafe / unsafe_self / allies) is generic *enough* to be reusable, but the bystander filter pulls in group / combat-handler concerns. Boundary needs discussion. |

## Out of scope (decided)

- **YAML / declarative content surface.** Unlike `evennia-mob-spawner` and `evennia-world-builder`, this library has no Reader, no Definitions, no Loader. Predicates and helpers are pure Python composed by the consumer. No CLI, no admin commands at v0.
- **Models / migrations / Django app surface.** The library ships an `apps.py` for `INSTALLED_APPS` hygiene but has no models, no `ready()` side effects, no admin commands. If a future need justifies admin commands, the `evennia._init` wrap pattern from sibling libraries is the path; it's not on the v0 roadmap.

## Open questions

Captured throughout the document as `[TBD]` markers. Summary:

- Exact set of predicates and helpers that move on first cut.
- Whether duck-typed visibility predicates are shipped with a pinned attribute contract.
- Whether `target_type` dispatch is library-side or consumer-side.
- Whether AoE secondary composition is library-side or consumer-side.
- Where the FCM mixin attribute reads (container / lockable / closeable / openable) land — pure library duck-typing vs consumer-side.

Each lands deliberately as the first real consumer for that piece appears.
