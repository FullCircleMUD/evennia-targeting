# SPDX-License-Identifier: BSD-3-Clause
"""Predicates — pure ``(obj, caller) -> bool`` filters.

Each predicate expresses a runtime-state filter that Evennia's native
``search()`` cannot. Composed by filtering a candidate list before
passing to ``caller.search(candidates=...)``.

**Predicates are added only when a real consumer needs them.** Do not
pre-populate this module with speculative filters.

**Before adding a new predicate:** check whether Evennia handles the
filter natively (tag/typeclass/attribute kwargs, the ``search`` lock,
``stacked``, multimatch disambiguation, ``location=`` scoping, etc).
Predicates exist ONLY for filters Evennia cannot express — runtime
state (hp, height, combat side), caller identity, typeclass EXCLUSION
(not inclusion), and runtime lock checks.

Scaffold: no predicates yet. The first predicates land when the
library's first real consumer (a port of FCM's targeting layer) is
ready to depend on them.
"""
