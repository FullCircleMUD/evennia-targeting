# SPDX-License-Identifier: BSD-3-Clause
"""evennia-targeting — composable targeting predicates and content-filtering helpers for Evennia.

Top-level package will export the symbols a consumer is expected to import
directly. Scope grows as predicates and helpers move from scaffold to real
implementation — current contents are the implemented surface only.

Tagline: *Composable targeting predicates and content-filtering helpers for
Evennia — layered on top of `caller.search()` rather than replacing it.*
"""

__version__ = "0.0.1"

__all__: list[str] = [
    "__version__",
]
