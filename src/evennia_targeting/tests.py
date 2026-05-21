# SPDX-License-Identifier: BSD-3-Clause
"""Smoke tests for evennia-targeting.

Verifies the library installs, the runner bootstraps, and the top-level
package exports its declared surface. Real unit tests for predicates
and helpers land alongside their implementations.
"""
import unittest


class PackageImportTest(unittest.TestCase):
    """The package imports cleanly under the test runner."""

    def test_package_imports(self):
        import evennia_targeting
        self.assertTrue(hasattr(evennia_targeting, "__version__"))

    def test_version_is_string(self):
        import evennia_targeting
        self.assertIsInstance(evennia_targeting.__version__, str)
