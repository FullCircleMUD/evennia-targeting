# evennia-targeting

Composable targeting predicates and content-filtering helpers for [Evennia](https://www.evennia.com/).

Predicates are pure `(obj, caller) -> bool` functions; helpers walk `room.contents` (or any container's contents) once, apply a predicate stack, and delegate string matching to Evennia's native `caller.search()`. The library expresses filters Evennia's native search kwargs cannot — runtime state (hp, height, combat side), caller identity, typeclass EXCLUSION (not inclusion), and runtime lock checks — without re-implementing anything Evennia already does well.

## Status

**Scaffold.** Repository scaffold is in place; library code is not yet written. The first predicates and helpers land when a real consumer (a port of FCM's in-game `utils/targeting/` package, decoupled from FCM-specific imports) is ready to depend on them. See [DESIGN/progress.md](DESIGN/progress.md) for the running milestone log.

## Is this for me?

This library is useful if you are building an Evennia game that:

- Wants to compose targeting filters as small, named predicates instead of inline lambdas scattered across commands.
- Wants a single-pass `room.contents` walk with predicate filtering for performance-sensitive code (look, scan, AI threat detection, AoE composition).
- Wants to keep Evennia's `caller.search()` doing what it does well (string matching, locks, nicks, multimatch, dbref) and only add filters Evennia can't natively express.

If your game's targeting is `caller.search(name)` everywhere and predicates have never been a need, you do not need this library.

## Install

The package is not on PyPI yet. Install directly from git:

```
pip install git+https://github.com/FullCircleMUD/evennia-targeting.git@main
```

## Learn more

- **[CLAUDE.md](CLAUDE.md)** — load-bearing principles and orientation for working in the repository.
- **[DESIGN/INDEX.md](DESIGN/INDEX.md)** — index of design documents.
- **[DESIGN/architecture.md](DESIGN/architecture.md)** — the library / consumer ownership boundary, predicate + helper surface shape, agreed decisions, open questions.

## License

BSD 3-Clause. See [LICENSE](LICENSE).
